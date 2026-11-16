import json,pathlib,re
P=pathlib.Path(__file__).parent
nodes=sum([json.loads((P/f'content_{x}.json').read_text()) for x in ['math','deep','core']],[])
alias={'m_vectors':'m_vector','ml_loss':'ml_mse','ml_generalization':'ml_bias_variance'}
for n in nodes:n['prereqs']=list(dict.fromkeys(alias.get(x,x) for x in n['prereqs']))
D={n['id']:n for n in nodes}
# Remove comparisons from the strict prerequisite DAG.
D['ml_clustering']['prereqs'].remove('ml_pca')
D['d_softmax']['prereqs']=['m_explog','m_vector']
D['v_dino']['prereqs'].remove('d_adam')
D['d_linear']['prereqs'].append('m_matmul')
D['p_gaussian']['prereqs'].append('m_explog')
D['v_selfsupervised']['prereqs']=['d_mlp','ml_mse','ml_bias_variance']

assert len(D)==len(nodes)
for n in nodes:
 for p in n['prereqs']:assert p in D,(n['id'],p)
# Ordering tracks strict conceptual dependencies, rather than the original broad level labels.
def rank(id,stack=()):
 assert id not in stack,('cycle',stack,id)
 n=D[id]
 if 'rank' not in n:n['rank']=max([rank(p,stack+(id,))+1 for p in n['prereqs']]+[0])
 return n['rank']
for n in nodes:rank(n['id'])
edges=[]
for n in nodes:
 for p in n['prereqs']:
  source=D[p]
  edges.append(dict(from_=p,to=n['id'],type='prereq',why=f'使用“{source["title"]}”中的{source["summary"].rstrip("。") }，理解“{n["title"]}”的建模与计算。具体代入目标节点公式，并检查符号所代表的数据形状。',formula=n['formula']))
for e in edges:e['from']=e.pop('from_')
for f in ['edge_math.json','edge_deep.json']:
 if (P/f).exists():
  for e in json.loads((P/f).read_text()):
   a=alias.get(e['from'],e['from']);b=e['to']
   for old in edges:
    if old['from']==a and old['to']==b:old.update(why=e['why'],formula=e.get('formula',''))
# Explanatory relations at the method and control boundaries.
why={
('m_explog','p_gaussian'):'高斯密度的指数项决定离均值越远密度如何下降；对数把指数密度转为便于优化的二次形式。',
('m_matmul','d_linear'):'全连接层逐个输出是输入与权重的点积，把这些点积一起写出就是矩阵乘法 Wx。',
('m_explog','d_softmax'):'先对每个分数取指数保证为正，再除以指数总和，得到和为一的权重。',
('d_mlp','v_selfsupervised'):'神经网络仍需一个可训练的映射；自监督改变监督信号的构造方式，不要求先学某一种视觉主干。',
('m_vector','r_frames'):'位置和方向先写成带参考系含义的向量，坐标变换才有明确的输入和输出。',
('r_state','r_dynamics'):'确定要预测的状态和可用动作后，才能定义动力学的一步输入输出，避免遗漏速度或接触。',
('r_state','r_goal'):'明确目标究竟包含积木位置、朝向还是推杆位置，才能选择相应误差与成功条件。',
('r_goal','r_search'):'搜索必须用目标代价比较候选动作序列，并用动作、碰撞和时间约束限制可接受的解。',
('r_state','r_policy'):'策略以状态或观察为输入，以环境动作为输出；价值也必须说明评估的是哪个状态或动作。',
('p_expectation','r_policy'):'未来奖励受状态转移和策略随机性影响，价值函数对这些可能轨迹的累计奖励取期望。',
('ml_bias_variance','r_offline'):'理解训练误差与泛化误差的差异，才能解释离线数据上拟合很好却在规划访问的新区域失效。',
('r_rollout','r_offline'):'多步想象会把模型误差继续传播，而规划又主动选择预测有利的轨迹，两种效应共同放大分布外风险。',
('m_vector','r_state'):'用向量把位置、角度、速度等量按约定顺序打包，才能定义模型输入、动作和预测目标。',
('m_matrix','r_frames'):'旋转是矩阵乘法，平移是向量加法；矩阵的行列及顺序决定坐标到底从哪个参考系转到哪个参考系。',
('m_derivative','r_dynamics'):'速度是位置对时间的导数，加速度是速度的导数；这些变化率把静态姿态连接到随时间变化的动力学。',
('p_conditional','r_markov'):'用条件概率表达“已知哪些历史后预测下一状态”，才能说明当前观察是否提供足够信息。',
('r_state','r_markov'):'如果状态里缺少速度或隐藏接触，单帧可能不足；历史窗口用先前观察和动作补充预测信息。',
('r_dynamics','r_feedback'):'动力学提供动作后果的预测；执行后用真实观察比较偏差并修改后续控制，形成反馈。',
('m_norm','r_goal'):'用范数把预测终点与目标之间的向量差压成一个数，供规划器比较不同候选序列。',
('r_dynamics','r_rollout'):'把一步状态转移反复调用构成多步预测，前一步的预测误差因此成为下一步模型的输入误差。',
('ml_mse','r_rollout'):'单步监督误差只检查一个转移；多步推演还需测误差如何随预测时长增长，二者指标不能互换。',
('p_sampling','r_search'):'连续动作空间无法逐个穷举，随机采样给出有限预算下探索候选序列的方法。',
('r_search','r_shooting'):'把高维搜索落成有限条动作候选，逐条打分；这是随机射击最基础的实现。',
('r_rollout','r_shooting'):'每条候选动作序列都需要模型连续向前预测，得到终点状态后才能计算代价并排序。',
('r_shooting','r_cem'):'保留采样、推演和打分流程；CEM 增加选择精英和重拟合采样分布，让后续搜索利用前轮结果。',
('p_gaussian','r_cem'):'使用可调均值和方差的高斯分布生成候选；精英样本的统计量用于更新下一轮采样参数。',
('p_expectation','r_cem'):'对精英样本求平均得到新的均值，对中心化平方求平均得到方差，这是重拟合的具体运算。',
('r_cem','r_mpc'):'CEM 解决一次有限时域优化；MPC 在实际执行和重新观察后反复调用这个优化器。',
('r_feedback','r_mpc'):'反馈把真实执行状态送回规划起点，避免一直沿用过时预测；MPC 规定如何反复规划和执行。',
('r_goal','r_reach'):'目标只说明想去哪；可达性还要检查是否存在满足动力学、障碍与动作约束的路径。',
('r_dynamics','r_reach'):'同样几何位置在不同速度或动作限制下，短时可达集合不同；可达性须包含时间和动力学。',
('ml_split','r_offline'):'按轨迹划分离线数据，检验规划访问的状态与训练覆盖是否不同，避免邻帧泄漏掩盖泛化问题。',
('g_conditional','i_high'):'将当前状态作为条件，将若干步后的状态作为生成目标，学习局部未来的多模态分布。',
('g_ddim','i_high'):'训练后用确定性 DDIM 将噪声映射到候选未来状态，使生成器能被高层规划反复调用。',
('r_reach','i_high'):'把生成目标限定为局部时间尺度下的未来，借数据学习可达结构；样本仍需低层执行和评测验证。',
('g_ddim','i_noise'):'固定模型和当前状态后，确定性采样器给出 z→未来状态的映射，因此搜索 z 就能选择候选子目标。',
('p_gaussian','i_noise'):'标准高斯给高层噪声提供采样先验；它没有逐维人工动作语义，异常幅值还可能造成分布外生成。',
('r_search','i_noise'):'用可搜索的连续噪声变量替代高层直接搜索漫长原始动作序列，把决策交给生成映射。',
('d_transformer','i_low'):'低层利用 Transformer 处理状态和动作历史，结合动作编码预测下一状态；上下文信息用于局部动力学。',
('r_rollout','i_low'):'对候选动作序列反复调用低层前向模型，预测末端状态与子目标的距离。',
('r_cem','i_low'):'CEM 提出并改进动作序列；前向模型负责评价后果，搜索过程完成目标到动作的逆向求解。',
('i_noise','i_objective'):'既然规划能主动修改噪声，就可能离开训练先验的常见区域，因此目标加入噪声幅值惩罚。',
('ml_regularization','i_objective'):'把目标距离与正则项加权相加，使“更接近目标”与“不要使用极端噪声”在同一评分中权衡。',
('r_goal','i_objective'):'用终点距离衡量目标误差，明确优化器要最小化的标量，再添加约束噪声的惩罚项。',
('r_search','i_hierarchy'):'长动作序列搜索维数随时域增长；高层子目标链把长程组织与局部动作优化分开。',
('i_high','i_hierarchy'):'从一个状态生成局部未来，再将该未来作为下一跳条件，才能将局部生成组合成子目标链。',
('r_reach','i_hierarchy'):'每一跳必须与低层时间预算匹配；仅仅几何上接近不代表低层能到达。',
('i_high','i_loop'):'高层训练使用时间间隔状态对，推理输出子目标候选；追踪这条数据流避免混淆标签和在线输入。',
('i_low','i_loop'):'低层训练使用动作条件的一步标签，推理通过多步候选评价选动作，训练与使用方向需分别记录。',
('r_mpc','i_loop'):'把两级搜索放进观察—执行—重新观察的循环，形成完整的在线推理与停止逻辑。',
('i_objective','i_loop'):'高层候选评分需同时计算目标误差和噪声正则，才能对 CEM 精英进行正确排序。',
('v_dinowm','i_compare'):'ID-WM 延续动作条件特征预测与规划的低层思路，并增加学习局部未来分布的高层来组织长程任务。',
('g_ddpm','i_compare'):'理解去噪建模后，才能比较生成整条轨迹与生成局部未来状态这两种不同的扩散用途。',
('r_policy','i_compare'):'策略和价值的概念帮助比较分层 RL 基线与依靠模型搜索的目标规划，辨别额外训练依赖。',
('ml_split','i_evaluate'):'固定训练、验证和测试边界，才能判断新目标表现来自泛化还是测试信息泄漏。',
('r_offline','i_evaluate'):'离线覆盖和规划分布差异影响成功率，因此评测需包括分布变化、失败以及数据增强设置。',
('i_loop','i_evaluate'):'清楚执行、重规划和搜索预算后，才能公平计算成功率、完成步数与端到端推理时间。',
('m_vector','e_python'):'数学向量落地为数组，先保留特征含义与顺序，再学习切片、广播和批量计算。',
('d_backprop','e_torch'):'自动微分实现链式法则，loss.backward 产生梯度，优化器据此更新模型参数。',
('e_python','e_torch'):'数组和函数操作转成张量与模块，必须同时管理形状、数据类型与设备位置。',
('ml_split','e_dataset'):'先按 episode 划分集合，再在内部取窗口，避免时间相邻帧或同轨迹未来跨越测试边界。',
('r_markov','e_dataset'):'历史窗口应包含预测所需的信息，同时保证窗口不跨 reset 且目标未来帧不进入输入。',
('e_python','e_dataset'):'用切片生成历史、动作与未来标签，再以可检查的数组形状组织批次。',
('e_torch','e_reproduce'):'训练闭环能运行只是第一步，还需保存配置、测量模型误差、评估闭环任务与计时。',
('e_dataset','e_reproduce'):'固定数据版本与窗口清单，才能让不同实验使用同一训练和评价输入。',
('i_evaluate','e_reproduce'):'从论文指标和消融设计反推复现验收项，避免只展示一段成功视频。',
('i_overview','e_project'):'把整体方法拆成数据、动力学、采样规划、层级连接和视觉扩展几个可独立验收的实践阶段。',
('e_reproduce','e_project'):'每个实践阶段都记录输入配置、预测误差、闭环指标与失败样本，让进步可以复查。'}
for e in edges:
 if (e['from'],e['to']) in why:e['why']=why[e['from'],e['to']]
 if e['to']=='i_overview':e['why']='把“'+D[e['from']]['title']+'”接入整体方法：'+D[e['from']]['summary']+'；在总览中追踪它的输入、输出及与另一层的接口。'
extra=[('d_rnn','d_lstm','evolution','LSTM 在循环状态更新中加入门与记忆通道，缓解长期梯度传播问题；它是 RNN 的改进结构。'),('d_cnn','d_rnn','parallel','CNN 利用局部空间结构，RNN 利用递归时间结构；两者可并行学习，谁先学由任务决定。'),('d_lstm','d_transformer','parallel','都能用于序列建模；Transformer 使用注意力而非循环更新，LSTM 不是理解其公式的强制先修。'),('v_dino','v_dinov2','evolution','DINOv2 发展了通用自监督视觉特征的训练和规模化思路；特征质量要在下游任务验证。'),('v_dinowm','i_low','evolution','沿用状态/视觉特征与动作历史预测下一状态并规划的低层思路，ID-WM 再添加高层组织。'),('g_ddpm','g_ddim','evolution','DDIM 提供与去噪训练相容的采样路径；确定性设置使初始噪声可以作为可搜索的高层变量。'),('r_mpc','i_hierarchy','evolution','保留有限时域优化与执行闭环，再引入子目标层，把长程路径组织与局部控制拆开。'),('r_dynamics','i_overview','application','机器人动力学可作为应用背景；论文主要实验在 Wall、PushT、Maze，迁移 G1 需额外状态、接触和控制验证。'),('ml_pca','g_latent','parallel','都涉及低维表示；PCA 使用线性最大方差投影，学习潜空间可以是非线性目标，不把 PCA 当作 DINO 必经训练步骤。'),('ml_pca','ml_clustering','parallel','PCA 可以为聚类提供预处理表示，但 K-means 和高斯混合本身不要求先做 PCA。'),('g_noise_action','i_noise','parallel','这两个节点分别从生成建模和算法决策解释同一桥梁，可对照检查噪声的角色。')]
for a,b,t,w in extra:edges.append(dict(from_=a,to=b,type=t,why=w,formula=''));edges[-1]['from']=edges[-1].pop('from_')
refs=[('ID-WM 原论文','https://arxiv.org/html/2610.42146v1'),('ID-WM 项目与演示','https://id-wm.github.io/'),('roadmap.sh：Machine Learning','https://roadmap.sh/machine-learning'),('D2L 动手学深度学习','https://zh.d2l.ai/'),('Mathematics for Machine Learning','https://mml-book.github.io/'),('MIT Underactuated Robotics','https://underactuated.mit.edu/'),('Modern Robotics','https://modernrobotics.northwestern.edu/'),('PyTorch 官方入门','https://docs.pytorch.org/tutorials/beginner/basics/intro.html')]
formal={}
for label in ['math','deep','core']:
 for entry in json.loads((P/f'formal_{label}.json').read_text()):formal[entry['id']]=entry
for node in nodes:
 original_title=node['title'];node.update({k:v for k,v in formal[node['id']].items() if k!='id'});node['title_original']=original_title
for entry in json.loads((P/'formal_edges.json').read_text()) if (P/'formal_edges.json').exists() else []:
 for edge in edges:
  if all(edge[k]==entry[k] for k in ['from','to','type']):edge['why_en']=entry['why_en']
from expansion_build import expand_atlas
nodes,edges,expansion=expand_atlas(P,nodes,edges)
import base64
figures={f.name:'data:image/png;base64,'+base64.b64encode(f.read_bytes()).decode() for f in (P/'paper_assets').glob('*.png')}
data=dict(**expansion,paperFigures=figures,nodes=nodes,edges=edges,references=[dict(title=t,url=u) for t,u in refs],version='4.1',date='2026-11-16')
(P/'dist').mkdir(exist_ok=True)
(P/'atlas.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
css=(P/'vendor/katex/dist/katex.min.css').read_text()
def font_data(m):
 file=P/'vendor/katex/dist'/m.group(1)
 mime={'woff2':'font/woff2','woff':'font/woff','ttf':'font/ttf'}[file.suffix[1:]]
 return 'url(data:'+mime+';base64,'+base64.b64encode(file.read_bytes()).decode()+')'
css=re.sub(r'url\((fonts/[^)]+)\)',font_data,css)
js=(P/'vendor/katex/dist/katex.min.js').read_text()
html=(P/'template.html').read_text().replace('__KATEX_CSS__',css).replace('__KATEX_JS__',js).replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
html += '\n<!-- KaTeX license follows\n'+(P/'vendor/katex/LICENSE').read_text().replace('--','- -')+'\n-->\n'
(P/'dist/index.html').write_text(html)
script=re.search(r'<script>\n(.*?)</script>',html,re.S).group(1);(P/'app-check.js').write_text(script)
print(json.dumps({'nodes':len(nodes),'edges':len(edges),'ranks':max(n['rank'] for n in nodes)+1,'characters':sum(len(n.get('explain',n['definition'])) for n in nodes),'missing_edge_explanations':len([e for e in edges if '具体代入目标节点公式' in e.get('why','')])},ensure_ascii=False))
