"""Typed topic taxonomy. Category membership and learning prerequisites are separate relations."""

def organize(nodes, edges):
    D={n['id']:n for n in nodes}
    homes={
      'ml_supervised':'ml_paradigms','v_selfsupervised':'ml_paradigms',
      'ml_mse':'loss_functions','wm_latent_prediction':'ml_objectives',
      'ml_linear':'ml_linear_models','ml_logistic':'ml_linear_models',
      'ml_kernel':'kernel_foundations','ml_pca':'ml_reduction','ml_clustering':'ml_probabilistic',
      'ml_split':'ml_validation','ml_bias_variance':'ml_validation','ml_evaluation':'ml_validation','ml_distribution_shift':'ml_validation','wm_uncertainty':'ml_validation',
      'ml_normalize':'ml_preprocessing','ml_regularization':'ml_training_methods',
      'd_backprop':'ml_autodiff','d_bptt':'ml_autodiff','d_sgd':'ml_optimization','d_adam':'ml_optimization','d_train_infer':'ml_training_methods',
      'g_flow_matching':'ml_training_methods','wm_target_encoder':'ml_training_methods',
      'd_mlp':'neural_architectures','d_cnn':'neural_architectures','d_rnn':'neural_architectures','d_lstm':'neural_architectures','d_transformer':'neural_components','g_autoencoder':'neural_architectures',
      'g_latent':'representation_basics','v_collapse':'representation_basics',
      'g_conditional':'generative_tasks','g_noise_action':'planning',
      'language_llm':'multimodal_systems','multimodal_contrastive':'ml_objectives','language_causallm':'ml_objectives','language_maskedlm':'ml_objectives','loss_hinge':'loss_functions','loss_huber':'loss_functions','language_nlp':'application_domains','domain_cv':'application_domains','cv_depth':'vision_tasks','cv_multiview':'vision_geometry','cv_sdf':'vision_representations','cv_gaussian_splat':'vision_representations','cv_scene_graph':'vision_representations','cv_affordance':'vision_representations','cv_tactile':'multimodal_representations','cv_inverse_rendering':'vision_tasks','cv_retrieval_memory':'inference_components','cv_tool_agent':'multimodal_systems','cv_information_gain':'planning','vla_vlm':'multimodal_systems','vla_action_tokens':'multimodal_representations',
      'vla_behavior_cloning':'ml_training_methods',
      'rl_mdp':'rl_foundations','rl_bellman':'rl_foundations','r_policy':'rl_foundations',
      'rl_actorcritic':'rl_algorithms','rl_ppo':'rl_algorithms'
    }
    for n in nodes:
        if n['id'] in homes:n['group']=homes[n['id']]
        elif n['group']=='deep':n['group']='neural_components'
        elif n['group']=='ml':raise ValueError('Unclassified legacy ML topic: '+n['id'])
        if n['group']=='world_model_papers':n['group']='world_papers'
        if n['group'] in ['ml_objectives','loss_functions']:n['entity_type']='objective'
        elif n['group']=='ml_paradigms':n['entity_type']='learning_paradigm'
        elif n['group'] in ['ml_training_methods','ml_autodiff','ml_optimization']:n.setdefault('entity_type','training_method')
        elif n['group']=='neural_components':n.setdefault('entity_type','architecture_component')
        elif n['group']=='neural_architectures':n.setdefault('entity_type','neural_architecture')
        elif n['group'] in ['ml_linear_models','ml_neighbors','ml_trees','ml_kernels','ml_probabilistic','ml_reduction','ml_clustering_models','generative']:n.setdefault('entity_type','model_family')
        elif n['group']=='multimodal_systems':n.setdefault('entity_type','system_family')
        elif n['group']=='language_foundations':n.setdefault('entity_type','language_concept')
        elif n.get('kind')=='paper':n['entity_type']='research_paper_or_release'
        else:n.setdefault('entity_type','concept')
    for id in ['ml_mse','loss_crossentropy']:
        if id in D:D[id]['usage_roles']=['training loss','evaluation metric']
    if 'ml_em' in D:D['ml_em']['entity_type']='training_algorithm'
    for id,en,zh in [('est_slam','SLAM Problem and System Structure','SLAM问题与系统结构'),('desc_ros2control','ros2_control Tags in URDF','URDF中的ros2_control标签')]:
        if id in D:D[id].update(en=en,title=zh)
    # Relationships identify how concepts compose; they do not assert that an objective is a model.
    semantic=[
      ('ml_pca','ml_unsupervised','trained_with','PCA estimates directions of variation from inputs without requiring task labels.'),
      ('ml_kmeans','ml_unsupervised','trained_with','k-means fits cluster assignments and centers without supplied class targets.'),
      ('ml_randomforest','ml_supervised','trained_with','Supervised forests fit regression or classification trees to labeled examples.'),
      ('ml_svm','loss_hinge','uses_objective','The soft-margin SVM combines a margin-based hinge objective with regularization.'),
      ('ml_logistic','loss_crossentropy','uses_objective','Bernoulli negative log-likelihood is binary cross-entropy for logistic regression.'),
      ('rl_ppo','ml_reinforcement','trained_with','PPO is a concrete policy-optimization algorithm within reinforcement learning.'),
      ('v_dino','train_distillation','training_component','DINO uses self-distillation with an evolving target encoder, rather than assuming a separately labeled fixed teacher.'),
      ('ml_clustering','ml_em','training_component','Expectation–maximization is a common parameter-fitting procedure for a Gaussian mixture model, not the mixture model itself.'),
      ('ml_linear','ml_supervised','trained_with','Linear regression is commonly fitted to labeled input–target pairs; supervised learning names this learning setup, not the predictor architecture.'),
      ('ml_linear','ml_mse','uses_objective','Least-squares fitting minimizes squared residuals. The linear predictor can also be fitted with other objectives.'),
      ('ml_logistic','ml_supervised','trained_with','Logistic regression learns a conditional class probability from labeled examples.'),
      ('g_vae','g_latent','training_component','A VAE introduces a latent-variable generative model and an approximate posterior; it is not a synonym for unsupervised learning.'),
      ('d_bptt','d_backprop','is_a','BPTT applies reverse-mode differentiation to an unrolled recurrent computation; recurrence can include neural states or differentiable dynamics.'),
      ('v_dino','v_selfsupervised','trained_with','DINO derives prediction targets from augmented views of input images without human class labels.'),
      ('paper_diffusion_policy','g_diffusion','training_component','Diffusion Policy uses conditional denoising to generate robot action trajectories; diffusion is a generative model family, not an application domain.'),
      ('vla_behavior_cloning','ml_supervised','trained_with','Behavior cloning uses demonstrated actions as supervised prediction targets.')
    ]
    for a,b,t,w in semantic:
        if a in D and b in D and not any(e['from']==a and e['to']==b and e['type']==t for e in edges):edges.append({'from':a,'to':b,'type':t,'why_en':w,'why':w})
    tax={}
    def add(id,en,zh,parent=None,children=(),rows=None,color='#6a8d79',axis='topic_family'):
        tax[id]=dict(id=id,en=en,title=zh,color=color,parent=parent,children=list(children),axis=axis)
        if rows is not None:tax[id]['childRows']=[list(r) for r in rows]
    roots=[
      ('math_root','Mathematics','数学','#748f64',['algebra','linear_algebra','calculus','geometry','probability','optimization','kernel_foundations']),
      ('learning_root','Learning & Training Foundations','学习与训练基础','#849267',['ml_paradigms','objective_design','ml_validation','ml_preprocessing','ml_training_methods','ml_autodiff','ml_optimization','rl_foundations','rl_algorithms']),
      ('models_root','Model Families & Architectures','模型家族与架构','#67888d',['classical_models','neural_models','generative']),
      ('domains_root','Vision, Language & Multimodal Systems','视觉、语言与多模态系统','#7a8aa0',['application_domains','representation_basics','vision','inference_components','language_foundations','multimodal_representations','multimodal_systems','generative_tasks']),
      ('robot_root','Robotics & Physics','机器人与物理','#6a8d79',['robot_basics','robot_description','robot_hardware','robotics_software','physics','kinematics','dynamics','control','estimation','perception','planning','motion','soccer']),
      ('simulation_root','Simulation & Sim-to-Real','仿真与迁移','#a28c62',['simulation']),
      ('systems_root','Computing & Training Systems','计算与训练系统','#8c7a65',['computing','cuda','pytorch_systems','training']),
      ('papers_root','Robotics, Vision & Learning Papers','机器人、视觉与学习论文','#7e7f9c',['world_papers','representation_papers','perception_papers','generative_papers','vla_papers','control_papers','motion_papers','soccer_papers','slam_papers','driving_papers'])]
    for id,en,zh,col,children in roots:add(id,en,zh,children=children,color=col)
    add('classical_models','Classical Machine Learning Models','传统机器学习模型','models_root',['ml_linear_models','ml_neighbors','ml_kernels','ml_trees','ml_probabilistic','ml_reduction','ml_clustering_models'],color='#67888d',axis='model_family')
    add('neural_models','Neural Architectures & Components','神经网络架构与组件','models_root',['neural_architectures','neural_components'],rows=[['neural_architectures'],['neural_components']],color='#67888d',axis='model_family')
    add('objective_design','Losses & Learning Objectives','损失与学习目标','learning_root',['loss_functions','ml_objectives'],color='#849267',axis='objective')
    add('vision','Computer Vision Concepts','计算机视觉概念','domains_root',['vision_tasks','vision_geometry','vision_representations'],color='#7a8aa0')
    labels={
      'algebra':('Algebra & Notation','代数与记号'),'linear_algebra':('Linear Algebra','线性代数'),'calculus':('Calculus & Differentiation','微积分与微分'),'geometry':('Geometry & Transformations','几何与变换'),'probability':('Probability & Statistics','概率与统计'),'optimization':('Optimization','优化'),'kernel_foundations':('Kernels & Feature Spaces','核函数与特征空间'),
      'loss_functions':('Loss Functions','损失函数'),'ml_paradigms':('Learning Paradigms','学习范式'),'ml_objectives':('Learning Objectives','学习目标'),'ml_validation':('Evaluation & Generalization','评估与泛化'),'ml_preprocessing':('Data Preparation','数据预处理'),'ml_training_methods':('Training & Transfer Methods','训练与迁移方法'),'ml_autodiff':('Differentiation Algorithms','微分与反向传播算法'),'ml_optimization':('Parameter Optimization','参数优化算法'),'rl_foundations':('Sequential Decision Foundations','序贯决策基础'),'rl_algorithms':('Reinforcement Learning Algorithms','强化学习算法'),
      'ml_linear_models':('Linear Predictors & Classifiers','线性预测与分类模型'),'ml_neighbors':('Instance-Based Models','基于实例的模型'),'ml_kernels':('Kernel Models','核方法模型'),'ml_trees':('Trees & Ensembles','树与集成模型'),'ml_probabilistic':('Probabilistic Models','概率模型'),'ml_reduction':('Decomposition & Dimensionality Reduction','分解与降维方法'),'ml_clustering_models':('Clustering Methods','聚类方法'),
      'neural_architectures':('Neural Network Architectures','神经网络架构'),'neural_components':('Neural Architecture Components','神经网络组件'),'generative':('Generative Model Families','生成模型家族'),
      'application_domains':('Application Domains','应用领域'),'vision_tasks':('Visual Estimation Tasks','视觉估计任务'),'vision_geometry':('Visual Geometry','视觉几何'),'vision_representations':('Spatial Representations','空间表征'),'inference_components':('Inference & Memory Components','推理与记忆组件'),'representation_basics':('Representation Concepts','表征基础'),'vision':('Computer Vision Concepts','计算机视觉概念'),'language_foundations':('Language & NLP Foundations','语言与NLP基础'),'multimodal_representations':('Multimodal Representations','多模态表征'),'multimodal_systems':('Language, Vision & Action Systems','语言、视觉与动作系统'),'generative_tasks':('Generation Tasks & Conditioning','生成任务与条件化'),
      'robot_basics':('States, Dynamics & Planning','状态、动力学与规划'),'robot_description':('Robot Descriptions & URDF','机器人描述与URDF'),'robot_hardware':('Robot Models & Hardware','机器人模型与硬件'),'robotics_software':('Robotics Software & Interfaces','机器人软件与接口'),'physics':('Classical Mechanics','经典力学'),'kinematics':('Robot Kinematics','机器人运动学'),'dynamics':('Robot Dynamics','机器人动力学'),'control':('Control Theory','控制理论'),'estimation':('State Estimation','状态估计'),'perception':('Perception & Mapping','感知与建图'),'planning':('Motion Planning','运动规划'),'motion':('Human Motion & Retargeting','人体运动与重定向'),'soccer':('Robot Soccer Systems','机器人足球系统'),
      'simulation':('Simulators & Transfer','仿真器与迁移'),'computing':('Computer Fundamentals','计算机基础'),'cuda':('GPU & CUDA Architecture','GPU与CUDA架构'),'pytorch_systems':('PyTorch Execution Stack','PyTorch执行栈'),'training':('Training Systems & Performance','训练系统与性能'),
      'world_papers':('World Models & Planning','世界模型与规划'),'representation_papers':('Representation Learning Papers','表征学习论文'),'perception_papers':('Vision & Perception Papers','视觉与感知论文'),'generative_papers':('Generative Models & Worlds','生成模型与世界'),'vla_papers':('VLA & Generalist Policies','VLA与通用策略'),'control_papers':('Learning & Control Papers','学习与控制论文'),'motion_papers':('Motion Recovery, Retargeting & Control','运动恢复、重定向与控制论文'),'soccer_papers':('Robot Soccer Research','机器人足球论文'),'slam_papers':('SLAM & Odometry Research','SLAM与里程计论文'),'driving_papers':('Driving-Adjacent Research','自动驾驶相关研究')}
    for parent in list(tax.values()):
        for g in parent['children']:
            if g in tax:continue
            if g not in labels:raise ValueError('Unknown taxonomy label '+g)
            add(g,*labels[g],parent=parent['id'],color=parent['color'])
    unknown=set(n['group'] for n in nodes)-set(tax)
    if unknown:raise ValueError('Unclassified groups: '+str(unknown))
    def populated(g):return any(n['group']==g for n in nodes) or any(populated(c) for c in tax[g]['children'])
    for g in list(tax):tax[g]['children']=[c for c in tax[g]['children'] if populated(c)]
    tax={g:v for g,v in tax.items() if populated(g)}
    tax['models_root']['childRows']=[['generative'],['neural_models'],['classical_models']]
    tax['domains_root']['childRows']=[['multimodal_systems','inference_components'],['vision','language_foundations'],['representation_basics','multimodal_representations'],['application_domains','generative_tasks']]
    rows=[['papers_root'],['domains_root','robot_root','simulation_root'],['models_root'],['learning_root','systems_root'],['math_root']]
    return tax,rows
