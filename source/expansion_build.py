"""Merge researched branches, normalize paper granularity, and classify reusable knowledge."""
import json,copy,re
from pathlib import Path

def expand_atlas(P,nodes,edges):
 nodes=copy.deepcopy(nodes);edges=copy.deepcopy(edges);base={n['id']:n for n in nodes}
 retired={n['id']:'i_overview' for n in nodes if (n['id'].startswith('i_') and n['id']!='i_overview') or n['id'] in ['e_reproduce','e_project']}
 def external_prereqs(id,seen=None):
  seen=set() if seen is None else seen
  if id in seen:return []
  seen.add(id);out=[]
  for p in base[id]['prereqs']:
   if p in retired:out+=external_prereqs(p,seen)
   else:out.append(p)
  return list(dict.fromkeys(out))
 base['i_overview']['prereqs']=external_prereqs('i_overview')
 base['i_overview']['kind']='paper';base['i_overview']['group']='world_papers';base['i_overview']['branch']='Latent dynamics and planning'
 base['i_overview']['paper']=dict(date='2026-10-30 (arXiv v1)',contribution='Composes local reachable-state generation with low-level action planning for long-horizon goal reaching.',architecture=[dict(label='Observation representation',node_id='r_state',role='Encode current and goal observations into compatible state or feature representations.'),dict(label='High-level diffusion generator',node_id='g_ddim',role='Map current state and selected initial noise to a local future state.'),dict(label='High-level and low-level CEM',node_id='r_cem',role='Search noise sequences for subgoals and action sequences for execution.'),dict(label='Action-conditioned forward model',node_id='d_transformer',role='Predict candidate local outcomes from state and action histories.'),dict(label='Execution feedback',node_id='r_mpc',role='Read actual observations after action blocks and replan according to the algorithm.')],training='Offline state pairs train the high-level denoiser; action-conditioned temporal windows train the low-level next-state predictor. Task rewards are not required for these dynamics objectives.',inference='CEM first searches diffusion-noise sequences for subgoals, then searches executable actions using low-level forward rollouts. Real execution updates the observed state.',evaluation='Wall, PushT and Maze suites. Success, object coverage, prediction quality, planning budgets and ablations belong to this paper record, not separate graph nodes.',scale='State-based low-level configuration reports a six-layer Transformer with eight heads. The full system parameter count is not explicitly summarized; visual experiments use a different backbone. Depth is not parameter count.',limitations='Finite offline coverage, model exploitation, subgoal executability and repeated planning cost remain relevant. Navigation/manipulation evidence does not establish humanoid soccer performance.',evidence_level='Public research paper and project demonstrations; no reproduction claim by this atlas.',sections=[dict(id=k,en=base[k]['en'],definition=base[k]['definition'],example=base[k]['example'],latex=base[k]['latex'],role_en=base[k]['role_en']) for k in retired])
 nodes=[n for n in nodes if n['id'] not in retired]
 research=[];new_edges=[];hardware_audits=[];unresolved_terms=[];course598={}
 for branch in ['foundations','systems','world','vla','learning','robotics_stack','urdf','humanoid_control','soccer_motion','ml_taxonomy','learning_roles','course598']:
  f=P/f'expansion_{branch}.json'
  if not f.exists():continue
  data=json.loads(f.read_text());research+=data.get('research',[]);new_edges+=data.get('edges',[]);hardware_audits+=data.get('hardware_audits',[]);unresolved_terms+=data.get('unresolved_terms',[]);course598=data.get('course598',course598)
  existing={n['id'] for n in nodes}
  for n in data['nodes']:
   if n['id'] in existing:
    # A researched paper may enrich a retained canonical identifier.
    if n.get('paper') or n.get('replaces'):
     next(x for x in nodes if x['id']==n['id']).update(n)
    continue
   n=copy.deepcopy(n);n.setdefault('kind','concept');n.setdefault('explain',n.get('definition',''));n.setdefault('formula',n.get('latex',''));n.setdefault('symbols','');n.setdefault('role',n.get('role_en',''));n.setdefault('pitfall','');n.setdefault('quiz','');n.setdefault('answer','');n.setdefault('sources',[]);n.setdefault('prereqs',[]);nodes.append(n);existing.add(n['id'])
 D={n['id']:n for n in nodes}
 # Original enabling architecture papers are units in their own right.
 if 'paper_transformer' not in D:
  t=copy.deepcopy(D['d_transformer']);t.update(id='paper_transformer',en='Attention Is All You Need (Transformer)',title='Transformer 原始论文',group='representation_papers',kind='paper',prereqs=['d_transformer'],sources=[dict(title='Attention Is All You Need',url='https://arxiv.org/abs/1706.03762')],paper=dict(date='2017-06-12 (arXiv v1)',contribution='Attention-only encoder–decoder sequence modelling with parallelizable training.',architecture=[dict(label='Token embeddings and positions',node_id='d_position',role='Provide content and token order.'),dict(label='Encoder attention and feed-forward blocks',node_id='d_transformer',role='Transform the input sequence with residual paths and normalization.'),dict(label='Masked decoder and cross-attention',node_id='d_self_attention',role='Predict outputs without observing future target tokens while reading encoder features.')],training='Teacher-forced sequence prediction with token-level supervised objectives.',inference='Autoregressively predicts output tokens in the original translation system.',evaluation='Machine translation and related sequence tasks in the source paper; robotic relevance is through the reusable architecture.',scale='Multiple model sizes are reported; do not equate one Transformer block with a full deployed model.',limitations='Dense attention has sequence-length cost and does not itself provide physical dynamics or control.',evidence_level='Public original paper; included as an enabling architecture rather than a robotics world model.'))
  nodes.append(t);D[t['id']]=t
 promotion={'v_vit':('representation_papers','2020-10-22','Vision Transformer uses image patches as tokens for a Transformer backbone.'),'v_dino':('representation_papers','2021-04-29','Self-distillation without labels learns visual representations using student and momentum-teacher predictions.'),'v_dinov2':('representation_papers','2023-04-14','Data curation and scaled self-supervised training produce broadly useful visual features.'),'v_dinowm':('world_papers','2024-11-07','Frozen DINOv2 patch features support action-conditioned world modelling and goal planning.'),'g_ddpm':('generative_papers','2020-06-19','Noise-prediction training learns a reverse denoising generative process.'),'g_ddim':('generative_papers','2020-10-06','An alternative sampling formulation enables deterministic generation under its zero-stochasticity setting.')}
 for id,(g,date,contribution) in promotion.items():
  n=D[id];n['kind']='paper';n['group']=g
  if not n.get('paper'):n['paper']=dict(date=date+' (arXiv v1; verify version at source)',contribution=contribution,architecture=[dict(label=D[p]['en'],node_id=p,role='See this prerequisite for the component definition and its relation to the paper.') for p in n['prereqs'][:4]],training=n['definition'],inference=n['role_en'],evaluation='See the original paper for protocol-specific results; this record keeps the evaluation attached to the method.',scale='Use the original paper and released checkpoint configuration for model-specific dimensions; no universal size is implied.',limitations='This component does not by itself establish a physically valid, closed-loop robot controller.',evidence_level='Public original paper and linked primary material.')
 # Classification assigns a primary home, while prerequisite and comparison edges express cross-field use.
 calculus={'m_derivative','m_partial','m_chain','m_gradient','m_jacobian'}
 geometry={'m_coordinates','m_trig','r_frames'}
 for n in nodes:
  n.pop('rank',None);n.setdefault('kind','concept');id=n['id']
  if id in ['m_gradient','c_constraints']:n['group']='optimization'
  elif id in ['rb_fk','rb_jacobian','rb_ik']:n['group']='kinematics'
  elif id in ['rb_inverse_dynamics','ph_manipulator']:n['group']='dynamics'
  elif id in ['ctrl_trajopt','ctrl_collision','ctrl_sampling_planners']:n['group']='planning'
  elif id in ['paper_beyondmimic','paper_videomimic']:n['group']='motion_papers'
  elif n.get('kind')=='paper' and 'jepa' in (id+' '+n['en']).lower():n['group']='representation_papers'
  elif n.get('kind')=='paper' and ('emma' in id.lower() or 'waymo' in id.lower() or 'gaia' in id.lower()):n['group']='driving_papers'
  elif n.get('kind')=='paper' and n['group']=='world_papers' and any(w in (id+' '+n.get('branch','')).lower() for w in ['cosmos','genie','giga','programmable','code_world','pwm','cwm','generative','video generation']):n['group']='generative_papers'
  elif id in calculus:n['group']='calculus'
  elif id in geometry:n['group']='geometry'
  elif n['group']=='math':n['group']='linear_algebra' if id not in ['m_function','m_explog','m_sum'] else 'algebra'
  elif n['group']=='prob':n['group']='probability'
  elif n['group']=='engineering':n['group']='computing'
  elif n['group']=='robot':n['group']='robot_basics'
  n['prereqs']=list(dict.fromkeys(retired.get(p,p) for p in n.get('prereqs',[]) if retired.get(p,p)!=id))
 # Separate camera calibration from depth API conventions and reconstruction.
 if 'sim_camera' in D and 'per_camera' in D:
  n=D['sim_camera'];n.update(en='Depth Conventions and Unprojection',title='深度约定与反投影',definition='Optical-axis depth measures a point’s camera-frame z coordinate; range measures its Euclidean distance from the camera center. They agree on the optical axis and differ away from it. Unprojection reconstructs a three-dimensional point from a calibrated pixel ray and one of these depth quantities. The formula must match the depth sensor or simulator API, image scaling, clipping rules and units. An invalid depth sample must be handled separately rather than reconstructed as an ordinary surface point.',latex=[r'r=K^{-1}[u,v,1]^{\top}',r'P_C=Z_C\,r\quad\text{or}\quad P_C=d_{\mathrm{ray}}\frac{r}{\|r\|_2}'],notation=[dict(symbol=r'K,u,v',meaning='Calibrated intrinsic matrix and distortion-corrected pixel coordinates.'),dict(symbol=r'r',meaning='Pinhole camera ray normalized to z component one, not unit Euclidean length.'),dict(symbol=r'P_C,Z_C,d_{\mathrm{ray}}',meaning='Camera-frame point, optical-axis depth and Euclidean range, in compatible metric units.')],role_en='Connects calibrated image geometry to depth-based reconstruction and simulator observations. Select the correct optical-depth or range formula before comparing robot perception and simulation.')
  n['latex']=[x.replace('\\\\','\\') for x in n['latex']]
  for x in n['notation']:x['symbol']=x['symbol'].replace('\\\\','\\')
  n['prereqs']=list(dict.fromkeys(n['prereqs']+['per_camera']))
  new_edges.append({'from':'per_camera','to':'sim_camera','type':'prereq','why_en':'Calibrated intrinsics define the pixel ray; the depth convention determines how to scale that ray into a metric point.'})
 cross_links={'g_flow_matching':['c_ode'],'paper_supermimic':['pt_vjp','concept_differentiable_dynamics','sim_mujoco','sim_warp'],'wm_planet':['wm_rssm'],'wm_dreamer':['wm_rssm','rl_actorcritic'],'wm_dreamerv2':['wm_rssm','rl_actorcritic'],'wm_dreamerv3':['wm_rssm','rl_actorcritic'],'wm_tdmpc':['rl_bellman'],'wm_tdmpc2':['rl_bellman'],'sim_warp':['gpu_kernel'],'sim_isaaclab':['r_policy','train_batch']}
 for id,ps in cross_links.items():
  if id in D:D[id]['prereqs']=list(dict.fromkeys(D[id]['prereqs']+[p for p in ps if p in D]))
 # New branch references are resolved explicitly after research rather than silently dropped.
 aliases=dict(retired)
 cross_alias={'m_vectors':'m_vector','ml_loss':'ml_mse','ml_generalization':'ml_bias_variance','m_integral':'c_integral','r_diffdynamics':'concept_differentiable_dynamics'}
 missing=[]
 for n in nodes:
  fixed=[]
  for p in n['prereqs']:
   p=cross_alias.get(p,p)
   if p not in D:missing.append((n['id'],p))
   else:fixed.append(p)
  n['prereqs']=list(dict.fromkeys(fixed))
 if missing:raise ValueError('Unresolved prerequisites: '+str(missing))
 # Rebuild strict prerequisite edges from final, condensed nodes.
 edge_lookup={}
 for e in edges+new_edges:
  a=retired.get(e.get('from',e.get('from_')),e.get('from',e.get('from_')));b=retired.get(e['to'],e['to'])
  if a in D and b in D and a!=b:edge_lookup[(a,b,e['type'])]=dict(e,**{'from':a,'to':b})
 E=[]
 for n in nodes:
  for p in n['prereqs']:
   edge=edge_lookup.get((p,n['id'],'prereq'),dict(from_=p,to=n['id'],type='prereq',why_en=f"{n['en']} uses {D[p]['en']} as specified by its definition, notation and method role."))
   edge['from']=p;edge.pop('from_',None);edge.setdefault('why_en',edge.get('why',''));edge['why']=edge.get('why',edge['why_en']);E.append(edge)
 for (a,b,t),edge in edge_lookup.items():
  if t!='prereq':edge['why']=edge.get('why',edge.get('why_en',''));E.append(edge)
 extra=[('ctrl_centroidal','motion_tracking','application','Centroidal momentum balance helps explain support and recovery constraints that a whole-body tracker must satisfy.'),('ctrl_wbc_qp','motion_tracking','parallel','Inverse-dynamics QP control and learned tracking policies are distinct approaches to realizing whole-body references; neither is an automatic drop-in replacement.'),('ctrl_impedance','soccer_foot_ball_contact','application','Stiffness and damping affect interaction forces, while short ball impacts still require contact and support dynamics.'),('desc_ros2control','ros2_control','application','URDF command-interface declarations configure the controller-manager and hardware-interface execution layer.'),('la_cross','ph_torque','application','A force applied at a lever arm creates a three-dimensional moment computed by the cross product.'),('paper_transformer','v_vit','evolution','ViT adapts the Transformer architecture to sequences of image patches.'),('v_dinov2','v_dinowm','application','DINO-WM uses frozen DINOv2 patch features as its predictive representation.'),('v_dinowm','i_overview','evolution','ID-WM retains action-conditioned local world modelling and adds a high-level local-future generator for hierarchical planning.')]
 for a,b,t,w in extra:
  if not any(e['from']==a and e['to']==b and e['type']==t for e in E):E.append(dict(from_=a,to=b,type=t,why_en=w,why=w));E[-1]['from']=E[-1].pop('from_')

 source_use={
 'd_transformer':'process ordered token or state-action histories with attention and feed-forward sublayers',
 'v_vit':'encode images as patch-token representations',
 'v_dinov2':'supply visual patch features for learned prediction or conditioning',
 'vla_vlm':'ground visual observations and language instructions in a shared pretrained representation',
 'g_flow_matching':'learn a conditional vector field for continuous action generation and integrate it at inference',
 'g_ddpm':'train conditional denoising from noisy examples and sampled noise targets',
 'g_ddim':'map fixed initial noise to a generated output under deterministic sampling settings',
 'g_diffusion':'represent multimodal predictions with iterative denoising rather than a single averaged output',
 'g_latent':'represent hidden or compressed variables used for prediction and generation',
 'p_gaussian':'specify a noise prior or proposal distribution from which model or planner inputs are sampled',
 'p_expectation':'average losses, returns or sample statistics over the relevant random variables',
 'p_conditional':'express how a future prediction depends on the information provided as context',
 'p_variance':'measure variation used in uncertainty, sampling or normalization',
 'p_likelihood':'evaluate probabilities or probability ratios for observed or sampled decisions',
 'r_state':'define observation, state and executable action interfaces without conflating them',
 'r_dynamics':'express the action-conditioned state transition being predicted or controlled',
 'r_rollout':'compose one-step predictions into a sequence, where model errors can propagate',
 'r_cem':'sample candidate decisions, select low-cost elites and refit a proposal distribution',
 'r_mpc':'connect finite-horizon model predictions to repeated observation and execution',
 'r_policy':'distinguish an action-selection policy and value estimate from a transition predictor',
 'r_offline':'identify finite data coverage and the distribution shift induced by planning',
 'd_backprop':'propagate training-loss derivatives through the executed network computation',
 'd_bptt':'propagate sensitivities through repeated temporal transitions',
 'm_chain':'compose derivatives across intermediate transformations',
 'm_jacobian':'represent local derivatives of vector-valued mappings or contract them with sensitivities',
 'm_matmul':'compute linear projections, batched dot products or state-space linear maps with compatible dimensions',
 'm_vector':'specify ordered numerical features and coordinate-wise decisions',
 'm_gradient':'collect parameter sensitivities and define a descent or ascent update',
 'ml_mse':'turn prediction residuals into a supervised error objective',
 'ml_split':'separate model selection and held-out evaluation from training data',
 'ml_bias_variance':'distinguish fitted training behaviour from generalization error',
 'd_mlp':'learn a nonlinear mapping through affine transformations and activations',
 'd_tensor':'organize batch, time and feature axes for compatible operations',
 'e_torch':'implement the forward, differentiation and parameter-update loop',
 'cs_memory':'separate weights, gradients, optimizer states, activations and workspace demand',
 'cs_parallel':'account for parallelizable work, dependencies and serial bottlenecks',
 'cs_floating':'account for rounding, exponent range and precision in numerical computation',
 'cs_storage':'connect logical tensor axes to the addresses and strides accessed by kernels',
 'gpu_kernel':'map logical tensor work onto a grid of blocks and threads',
 'gpu_simt':'reason about warp execution, scheduling and divergence',
 'gpu_hierarchy':'reason about capacity, locality and data reuse across GPU storage levels',
 'pt_graph':'track executed differentiable operations and the lifetime of saved intermediate tensors',
 'pt_streams':'establish ordering and completion across asynchronous host and device execution',
 'train_batch':'relate microbatches and gradient normalization to a complete optimizer update',
 'train_ddp':'coordinate corresponding states or gradients across parallel workers',
 'rl_bellman':'construct continuation-value targets rather than treating a finite rollout as the full return',
 'rl_actorcritic':'separate policy improvement from return or value estimation',
 'wm_rssm':'separate observation-conditioned latent inference from prior-driven future imagination',
 'wm_uncertainty':'compare predicted outcomes and model uncertainty before committing to a planned action',
 'concept_differentiable_dynamics':'differentiate policy objectives through a learned state transition model',
 'pt_vjp':'compute reverse-mode vector-Jacobian products without materializing full Jacobians',
 }
 for edge in E:
  target=D[edge['to']];source=D[edge['from']];text=edge.get('why_en','')
  if any(x in text for x in ['as specified by','uses this foundation','receiving formula']):
   module=next((m for m in target.get('paper',{}).get('architecture',[]) if m.get('node_id')==edge['from']),None)
   if module:edge['why_en']=f"The {module['label']} component uses {source['en']}: {module['role']}"
   elif edge['from'] in source_use:edge['why_en']=f"{target['en']} uses {source['en']} to {source_use[edge['from']]}.'".rstrip("'")
   else:edge['why_en']=f"{source['en']} supplies a prerequisite for {target['en']}; the receiving definition specifies the variables and assumptions used together."
   edge['why']=edge['why_en']
 for node in nodes:
  if node.get('paper') and 'jepa' in node['en'].lower():
   for module in node['paper'].get('architecture',[]):
    if 'target encoder' in module.get('label','').lower() and 'wm_target_encoder' in D:module['node_id']='wm_target_encoder'
 visiting=set()
 def rank(id):
  n=D[id]
  if 'rank' in n:return n['rank']
  if id in visiting:raise ValueError('Prerequisite cycle at '+id)
  visiting.add(id);n['rank']=max([rank(p)+1 for p in n['prereqs']]+[0]);visiting.remove(id);return n['rank']
 for n in nodes:rank(n['id'])
 # Course membership is a collection, separate from scientific taxonomy.
 for session in course598.get('sessions',[]):
  for reading in session.get('readings',[]):
   id=reading.get('node_id')
   if id in D:
    node=D[id];node.setdefault('course_topics',[]);node.setdefault('course_speakers',[])
    node['course_topics']=list(dict.fromkeys(node['course_topics']+[session['topic']]))
    node['course_speakers']=list(dict.fromkeys(node['course_speakers']+[s['name'] for s in session.get('speakers',[])]))
 from taxonomy_build import organize
 tax,overview_rows=organize(nodes,E)
 return nodes,E,dict(aliases=aliases,taxonomy=tax,overviewRows=overview_rows,research=research,course598=course598,hardwareAudits={a['id']:a for a in hardware_audits},coverage=dict(checked_date='2026-11-16',scope='Robotics, perception and learning foundations, selected influential/recent primary-source research, and an explicit course reading collection; curated rather than exhaustive or popularity-ranked.',granularity='One paper or official release per paper node. Evaluation, scale and implementation guidance stay inside that paper. Reusable concepts have independent nodes.',unresolved_terms=unresolved_terms+[dict(term='Waymo-VLA',status='Exact intended work is not uniquely identified. Verified Waymo EMMA and Waymo World Model are separate records, not asserted aliases.')]))
