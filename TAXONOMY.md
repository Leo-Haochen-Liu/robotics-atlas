# Record types and connection conventions

The main navigation now has a stable course-based Foundations map and a topic-based Research map. The types below describe records and relationships; they are not separate top-level browsing areas. Papers and methods for one research field are co-located. See [the curriculum](CURRICULUM.md) and [coverage audit](COVERAGE_AUDIT.md).

The atlas uses several independent classification axes, not a claim that all of machine learning has one universal tree. A node has one primary browsing location and typed cross-links for other roles. Category depth describes browsing scope; solid prerequisite arrows describe learning dependencies.

| Axis | Question | Examples |
| --- | --- | --- |
| Learning paradigm | What feedback or supervision defines learning? | supervised, unsupervised, self-supervised, reinforcement learning |
| Model family / architecture | What mathematical mapping or distribution is represented? | linear regression, random forest, GMM, CNN, VAE |
| Objective / loss | What quantity is optimized or measured? | MSE, classification cross-entropy, hinge loss, predictive latent objectives |
| Training method / algorithm | How are parameters or representations fitted or transferred? | EM, backpropagation, BPTT, distillation, fine-tuning, LoRA |
| Application domain | What kind of problem is studied? | computer vision, NLP, robotics |
| System family | What information interface and capabilities are combined? | LLM, VLM, VLA, world model |

Linear regression is a model commonly trained in a supervised setup. Least-squares fitting uses MSE; that does not make MSE a model or make every linear predictor require MSE. MSE can also be an evaluation metric. PCA is a dimensionality-reduction method. A Gaussian mixture is a model; EM is a fitting algorithm. VAE is a latent-variable generative model with a neural inference network; it is not a learning paradigm. BPTT differentiates an unrolled recurrent computation and can be used for differentiable dynamics as well as RNNs.

| Connection | Meaning |
| --- | --- |
| prerequisite | Learning the receiving definition or derivation uses the source concept. |
| trained with | A model or method uses the named learning setup. |
| uses objective | The specified fitting procedure uses that objective; alternatives may exist. |
| training component | A system uses a reusable training procedure or component. |
| specialization | The source is a specific form of the target concept. |
| evolution / parallel / application | Method development, comparison or reuse, with a written explanation. |

Model-family folders show classical models toward the bottom and neural/generative families above them. This is a pedagogical organization, not a claim that every modern model mathematically depends on every classical algorithm. CV, NLP, LLMs, VLMs, VLAs, diffusion and world modelling overlap along different axes; the atlas does not force them into one historical chain.

Course readings are a separate collection. Papers remain in their scientific branches, and presenter association is recorded separately from authorship. This prevents a course or source collection from being confused with a model family.

The organization is informed by the [U-M EECS545 syllabus](https://web.eecs.umich.edu/~honglak/teaching/eecs545/) and the primary texts and papers linked at each node. It is an editorial learning framework, not an official taxonomy issued by the university.
