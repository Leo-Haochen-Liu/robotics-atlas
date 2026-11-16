"""Course-anchored foundations and topic-centered research share canonical knowledge records."""
import json,re
from collections import defaultdict

def build_curriculum(P,nodes,edges,course598):
 D={n['id']:n for n in nodes};courses=[];gaps=[]
 for f in sorted(P.glob('curriculum_*.json')):
  data=json.loads(f.read_text());courses+=data.get('courses',[])
  raw_gaps=data.get('gaps',[])
  if isinstance(raw_gaps,dict):
   for status,items in raw_gaps.items():
    if not isinstance(items,list):continue
    for item in items:
     item=dict(item);item.setdefault('status',status);item.setdefault('title',item.get('topic',D.get(item.get('node_id'),{}).get('en','Coverage note')))
     if item.get('node_id'):item.setdefault('node_ids',[item['node_id']])
     gaps.append(item)
  else:gaps+=raw_gaps
 course_by={c['id']:c for c in courses}
 membership=defaultdict(list)
 for c in courses:
  c.setdefault('source_urls',c.get('sources',[]));c.setdefault('anchor',c['title']);c.setdefault('scope','Course-anchored editorial knowledge mapping; not an official lecture transcript.')
  for i,m in enumerate(c['modules']):
   m['id']=m.get('id',str(i));m['id']=m['id'] if m['id'].startswith(c['id']+'__') else c['id']+'__'+m['id'];m.setdefault('zh',m['title']);m.setdefault('summary','');m.setdefault('learning_outcome','')
   unknown=[id for id in m['node_ids'] if id not in D]
   if unknown:raise ValueError('Unknown course node references '+c['id']+': '+str(unknown))
   m['reading_ids']=[id for id in m['node_ids'] if D[id]['kind']=='paper']
   m['node_ids']=[id for id in m['node_ids'] if D[id]['kind']!='paper']
   if not m['node_ids'] and m['reading_ids']:
    m['node_ids']=list(dict.fromkeys(p for id in m['reading_ids'] for p in D[id]['prereqs'] if D[p]['kind']!='paper'))
    m['mapping_note']='These concepts are atlas prerequisites for the listed readings, not a claim about exact lecture coverage.'
   for id in m['node_ids']+m['reading_ids']:membership[id].append(dict(course_id=c['id'],module_id=m['id']))
 # Reviewed stable supplements do not change when new research papers are catalogued.
 supplements=json.loads((P/'foundation_supplements.json').read_text())['course_node_ids']
 for cid,ids in supplements.items():
  if cid not in course_by:continue
  ids=[id for id in ids if id in D and D[id]['kind']!='paper']
  m=dict(id=cid+'__atlas_supplement',title='Additional Atlas References',zh='补充知识索引',node_ids=ids,reading_ids=[],summary='Related catalogued concepts outside the explicit mapped modules.',learning_outcome='Use these cross-references as needed; their inclusion does not assert coverage in the anchor syllabus.',mapping_note='Atlas supplement, not an official course module.')
  course_by[cid]['modules'].append(m)
  for id in ids:membership[id].append(dict(course_id=cid,module_id=m['id']))
 nav={}
 def add(id,title,zh,parent=None,children=(),ids=(),**kw):
  nav[id]=dict(id=id,en=title,title=zh,color=kw.pop('color','#6a8d79'),parent=parent,children=list(children),node_ids=list(ids),**kw)
 areas=[('f_math','Mathematics','数学','SI602 · ROB501 · Math Bridges',['course_math','course_si602','course_rob501','course_math_bridge']),('f_robotics','Robot Mechanics & Control','机器人力学与控制','Modern Robotics + control supplements',['course_modern_robotics']),('f_ml','Machine Learning','机器学习','EECS545',['course_eecs545']),('f_rl','Deep Reinforcement Learning','深度强化学习','Berkeley CS285',['course_cs285']),('f_cv','Computer Vision','计算机视觉','Stanford CS231n',['course_cs231n']),('f_action','Action & Perception','行动与感知','CSE598',['course_cse598']),('f_sim','Simulation & Sim-to-Real','仿真与迁移','CSE598 themes + simulator foundations',['course_simulation']),('f_engineering','Engineering & Research Practice','工程与研究实践','Systems · integration · reproducibility',['course_engineering'])]
 assigned={id for a in areas for id in a[4]}
 for c in courses:
  if c['id'] not in assigned:
   target=1 if any(s in c['id'] for s in ['control','underactuated','manipulation','autonomy','estimation','planning']) else 7
   areas[target][4].append(c['id'])
 for aid,title,zh,anchor,cids in areas:
  cs=[course_by[x] for x in cids if x in course_by]
  if not cs:continue
  add(aid,title,zh,anchor=anchor,kind='foundation_area',course_ids=[c['id'] for c in cs])
  # A single anchor opens directly into its modules.
  for c in cs:
   parent=aid
   if len(cs)>1:
    add(c['id'],c['title'],c.get('zh',c['title']),aid,kind='course',course_id=c['id'],anchor=c['anchor']);nav[aid]['children'].append(c['id']);parent=c['id']
   for m in c['modules']:
    mid='module_'+m['id'];add(mid,m['title'],m['zh'],parent,ids=m['node_ids'],kind='module',course_id=c['id'],module_id=m['id'],reading_ids=m['reading_ids']);nav[parent]['children'].append(mid)
   nav[parent]['childRows']=[nav[parent]['children'][i:i+2] for i in range(0,len(nav[parent]['children']),2)][::-1]
 foundation_rows=[[x for x in row if x in nav] for row in [['f_action','f_sim','f_rl'],['f_robotics','f_cv','f_ml'],['f_math','f_engineering']]]
 specs=[('soccer','Robot Soccer','机器人足球','Ball perception, approach, contact, recovery and team play.',['soccer_ball_state','soccer_foot_ball_contact','soccer_active_vision','soccer_skill_chaining','soccer_multiagent','motion_tracking','rl_ppo','est_kalman','per_latency','hw_g1_29','hw_go2','hw_t2_31']),('motion','Motion, Retargeting & Humanoids','运动、重定向与人形控制','Recover human motion, retarget references and train executable whole-body feedback.',['motion_smpl','motion_retargeting','motion_tracking','motion_prior','motion_contact_quality','concept_differentiable_dynamics']),('manipulation','Manipulation & Interaction','操作与物理交互','Plan and control object interaction, dexterous contact and task completion.',['rb_ik','ctrl_impedance','ctrl_wbc_qp','cv_affordance','cv_tactile','r_mpc']),('vla','Vision–Language–Action','视觉语言动作','Connect observations, language and executable robot actions.',['system_vla','vla_vlm','vla_behavior_cloning','vla_action_chunk','vla_action_tokens','g_flow_matching','train_distillation','vla_embodiment']),('world_models','World Models & Planning','世界模型与规划','Predict action consequences and choose actions or subgoals.',['system_world_model','r_dynamics','r_rollout','r_cem','r_mpc','g_diffusion','g_flow_matching','wm_rssm','wm_uncertainty']),('perception','Perception, Geometry & SLAM','感知、几何与SLAM','Estimate scene geometry, object motion and robot state.',['per_camera','per_extrinsics','est_slam','est_vio','est_lio','est_factorgraph','cv_depth','cv_multiview']),('representations','Representation Learning','表征学习','Learn visual, temporal and multimodal representations usable by robot systems.',['v_selfsupervised','wm_latent_prediction','wm_target_encoder','multimodal_contrastive','g_latent','v_collapse']),('simulation','Simulation & Data Generation','仿真与数据生成','Build environments, generate training data and study simulation transfer.',['sim_mujoco','sim_isaaclab','sim_warp','sim_camera','desc_urdf','sim_domain_randomization']),('reliability','Reliability, Evaluation & Safety','可靠性、评估与安全','Study uncertainty, distribution shifts, robustness and trustworthy evaluation.',['ml_evaluation','ml_distribution_shift','ml_split','wm_uncertainty','ctrl_runtime_limits'])]
 topic_by={id:dict(id=id,title=en,zh=zh,summary=summary,method_ids=[x for x in seeds if x in D],paper_ids=[]) for id,en,zh,summary,seeds in specs}
 session_topics={
  'Visual Representations of Images and Videos':'representations',
  'Visual Representation of Depth and 3D':'perception',
  'Robot Learning from Multimodal Experiences for Dexterity':'manipulation',
  'Bridging the Interaction Gap: Low-Level Control in Large-Scale Procedural Worlds':'manipulation',
  'Visual Space Perception and Nonlinear Perceptual Geometries':'perception',
  'Object-Centric Embodied 3D Vision':'perception',
  'Robots That Learn from Experience':'manipulation',
  'Building Agentic Robotics Systems: Reasoning, Tools, Infrastructure, and Reinforcement Learning':'manipulation',
  'Towards Reliable Dexterity with Less Data':'manipulation',
  'From SLAM to Spatial AI: Mapping, Memory, and Reasoning':'perception',
  'Foundation Models for Unified Multimodal Understanding and Generation':'representations',
  'Game-ready 3D Asset Generation':'simulation',
  'From Pixels to Physics: Understanding and Manipulating Physics from Images':'simulation',
  'What’s Missing in Multimodal AI? Towards Spatial Awareness, Effective Tool Use and Fine-Grained Understanding':'representations',
  'Learning Human and Robot Motions':'motion',
  'The Role of Geometry in Large-Scale 3D Learning':'perception',
  'Memory for Robotics':'vla',
  'World-Action Models for Contact-Rich Robotic Manipulation':'world_models',
  'Beyond Plausible: Physically Valid Human-Object Interaction for Robot World Models':'world_models',
  'Perception You Can Act On: Reliability, Attack Surfaces, and Active Multimodal Agents':'reliability'}
 def primary(n):
  text=(n['en']+' '+n['id']).lower();ctx=' '.join(n.get('course_topics',[])).lower();g=n['group']
  if g=='soccer_papers':return 'soccer'
  if n['id'] in ['paper_sage','paper_foragebench','paper_scenesmith']:return 'simulation'
  contextual=next((session_topics[t] for t in n.get('course_topics',[]) if t in session_topics),None)
  if contextual:return contextual
  if any(x in text for x in ['adversarial','conformal','factuality','harmful','sound-break','sound_break','lamp:']):return 'reliability'
  if any(x in text for x in ['scenesmith','scene generation','asset generation','articulate','procedura','sage:','foragebench']):return 'simulation'
  if g=='motion_papers' or 'supermimic' in text:return 'motion'
  if g=='vla_papers' or any(x in text for x in ['vla','vtam','memory for robot','memory robot','memor','gen-1.5']):return 'vla'
  if g in ['world_papers','generative_papers']:return 'world_models'
  if g=='representation_papers':return 'representations'
  if g in ['slam_papers','driving_papers']:return 'perception'
  if any(x in text for x in ['manipulation','dexter','tactile','grasp','visuomotor','contact','robot learning','behavioral cloning','behavioural cloning','physics','robot-factored','robot_factored']):return 'manipulation'
  if g=='control_papers':return 'manipulation'
  return 'perception'
 excluded={'algebra','linear_algebra','calculus','geometry','probability','optimization','kernel_foundations','computing','cuda','pytorch_systems','training','ml_objectives','loss_functions','ml_validation','ml_preprocessing'}
 for n in nodes:
  if n['kind']!='paper':continue
  tid=primary(n);topic_by[tid]['paper_ids'].append(n['id'])
  if n['id'] in ['paper_humanx','paper_beyondmimic','paper_supermimic']:topic_by['soccer']['paper_ids'].append(n['id'])
 for t in topic_by.values():
  for id in t['paper_ids']:
   for p in D[id]['prereqs']:
    if D[p]['kind']!='paper' and D[p]['group'] not in excluded:t['method_ids'].append(p)
  t['method_ids']=list(dict.fromkeys(t['method_ids']));t['paper_ids']=list(dict.fromkeys(t['paper_ids']))
  t['course_ids']=list(dict.fromkeys(m['course_id'] for id in t['method_ids'] for m in membership[id]))
 research_nav={};node_topics=defaultdict(list)
 for t in topic_by.values():
  rid='research_'+t['id'];research_nav[rid]=dict(id=rid,en=t['title'],title=t['zh'],parent=None,children=[rid+'_papers',rid+'_methods'],node_ids=[],color='#7e7f9c',kind='research_topic',topic_id=t['id'],anchor='Methods + papers in one topic')
  for suffix,title,zh,ids in [('papers','Papers & Systems','论文与系统',t['paper_ids']),('methods','Methods & Prerequisites','方法与预备知识',t['method_ids'])]:
   gid=rid+'_'+suffix;research_nav[gid]=dict(id=gid,en=title,title=zh,parent=rid,children=[],node_ids=ids,color='#7e7f9c',kind='research_papers' if suffix=='papers' else 'research_methods',topic_id=t['id'],sort='newest' if suffix=='papers' else 'prerequisite')
  research_nav[rid]['childRows']=[[rid+'_papers'],[rid+'_methods']]
  for id in t['method_ids']+t['paper_ids']:node_topics[id].append(t['id'])
 research_rows=[['research_soccer','research_motion','research_manipulation'],['research_vla','research_world_models','research_perception'],['research_representations','research_simulation','research_reliability']]
 unmapped=[n['id'] for n in nodes if n['kind']!='paper' and not membership[n['id']]]
 return dict(courses=courses,gaps=gaps,topics=list(topic_by.values()),node_courses=dict(membership),node_topics=dict(node_topics),views={'foundations':dict(taxonomy=nav,rows=[r for r in foundation_rows if r]),'research':dict(taxonomy=research_nav,rows=research_rows)},coverage=dict(nonpaper_nodes=sum(n['kind']!='paper' for n in nodes),mapped_foundation_nodes=len([n for n in nodes if n['kind']!='paper' and membership[n['id']]]),unmapped_foundation_nodes=unmapped,research_papers=sum(n['kind']=='paper' for n in nodes)),maintenance=dict(foundations='Stable course anchors and modules; revise deliberately when a better course or a missing foundation is identified.',research='Extend paper records and topic links independently of the foundation curriculum. No automatic update schedule is implied.'))
