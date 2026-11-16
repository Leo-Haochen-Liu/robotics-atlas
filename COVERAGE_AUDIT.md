# Curriculum coverage audit

An audit of learning references and remaining lesson depth, not a certification of competence or a claim of an exhaustive curriculum.

Framework references: [CMU robotics curriculum](https://www.ri.cmu.edu/education/academic-programs/master-of-science-robotics/curriculum/), [Stanford robot autonomy](https://bulletin.stanford.edu/courses/2185453).

## Sets, Logic, Quantifiers and Proof

High-school-to-university entry point for event notation, research assumptions, and ROB501 proof work.

Status: filled


## Counting, Combinations and Binomial Coefficients

Fills SI602 Units1–2 and the counting prerequisite for discrete distributions and probability spaces.

Status: filled


## Span, Independence, Basis, Rank and Null Space

Connects SI602 linear algebra to least squares, SVD, state identifiability, observability, and research proof language.

Status: filled


## Orthogonal Projection, QR and Least Squares

Fills the mathematical mechanism between matrix multiplication and regression/estimation in ROB501, Math51, and EE263.

Status: filled


## Limits, Convergence and Fixed-Point Iteration

Provides ROB501 analysis language and a bridge from computational updates to convergence claims in optimization, solvers, and filtering.

Status: filled


## Convexity and Jensen’s Inequality

Fills the CSE598 preparation link among expectation, nonlinear functions, log objectives, and convex optimization.

Status: filled


## Joint Distributions, Densities, CDFs and Marginals

Connects calculus to continuous probability, CSE598 Gaussian preparation, mixture models, latent variables, and filtering.

Status: filled


## Estimation, Confidence Intervals and Hypothesis Tests

Adds the SI602 significance/confidence link and supports honest algorithm evaluation without reproducing any private assessment.

Status: filled


## Conditioning, Residuals and Numerical Stability

Connects SVD and floating-point computation to reliable implementation of estimation, inverse kinematics, and training algorithms.

Status: filled


## Complex Numbers and Complex Exponentials

Provides the assumed complex-number background in ROB501 and the signals/dynamics bridge in Berkeley EECS16 and Stanford EE363.

Status: filled


## Determinants, elimination, LU and Cholesky

Course maps reference these foundations, but dedicated fine-grained nodes and worked numerical examples remain useful; not silently claimed complete.

Status: partially represented


## Real-analysis details: open/closed sets, completeness, compactness

ROB501 covers these explicitly; the new convergence node gives an entry point, not a full analysis course.

Status: overview only


## Newton, Gauss–Newton, duality, LP/QP and interior-point algorithms

The course paths expose where to study them; dedicated solver derivations and worked numerical examples remain to be developed in the atlas.

Status: distributed across overview nodes


## Concentration, LLN/CLT, confidence procedures and multiple testing

Different statistical results require distinct assumptions and future dedicated derivations.

Status: inference entry point only


## Graph mathematics, Markov chains and PageRank

A scene graph and an HMM are applications, not substitutes for a full graph/Markov-chain foundation.

Status: applications linked; dedicated basics incomplete


## Fourier transforms, convolution and sampling theory

The current expansion explains entry points without pretending these linked application nodes teach the full theory.

Status: complex-number prerequisite added; spectral course incomplete


## Measure-theoretic probability and stochastic processes

Not required before every applied robotics paper, but relevant to deeper probabilistic research.

Status: advanced optional extension


## Core deep-RL update mechanisms

The prior graph had MDP/Bellman, actor–critic and PPO but omitted core explanations needed to compare value-based, off-policy, model-based and offline methods.

Status: added_in_this_revision

- [Berkeley CS185/285 Spring 2026 schedule](https://rail.eecs.berkeley.edu/deeprlcourse/)

## Pixel-level segmentation tasks

Dense object regions and task-specific metrics are required before treating segmentation or scene-model papers as understood.

Status: added_in_this_revision

- [Stanford CS231n Spring 2026 schedule](https://cs231n.stanford.edu/schedule.html)

## Dynamic programming and policy/value iteration derivations

The Bellman node provides the relation, but tabular policy evaluation/improvement, value iteration, contraction assumptions and exact-vs-approximate guarantees need a dedicated worked unit.

Status: still_missing

- [Berkeley CS185/285 Spring 2026 schedule](https://rail.eecs.berkeley.edu/deeprlcourse/)

## Multi-task, goal-conditioned and hierarchical RL

Task-conditioned objectives, goal relabeling and temporal abstraction need distinct definitions before multi-task papers can be compared.

Status: still_missing

- [Berkeley CS185/285 Spring 2026 schedule](https://rail.eecs.berkeley.edu/deeprlcourse/)

## RL learning theory and off-policy evaluation

Coverage, concentrability, sample complexity and evaluation-estimator assumptions are not fully developed by the current empirical algorithm explanations.

Status: still_missing

- [Berkeley CS185/285 Spring 2026 schedule](https://rail.eecs.berkeley.edu/deeprlcourse/)

## Preference modeling, inverse RL and LLM post-training

The Spring2026 course includes LLM-RL and inverse-RL discussion, but language backbones and generic PPO do not define reward models, preference data or their evaluation.

Status: still_missing

- [Berkeley CS185/285 Spring 2026 schedule](https://rail.eecs.berkeley.edu/deeprlcourse/)

## Generative adversarial networks

A GAN generator/discriminator game is distinct from VAE and diffusion objectives and is named in the current CS231n generative module.

Status: still_missing

- [Stanford CS231n Spring 2026 schedule](https://cs231n.stanford.edu/schedule.html)

## Dedicated video-recognition foundations

Generic temporal models and tracking do not fully explain 3D convolutions, two-stream motion features, temporal sampling or video-recognition evaluation.

Status: still_missing

- [Stanford CS231n Spring 2026 schedule](https://cs231n.stanford.edu/schedule.html)

## Visual interpretation and adversarial robustness

Saliency/feature inversion and adversarial examples need objective- and threat-model-specific explanations before using newer robustness papers.

Status: still_missing

- [Stanford CS231n Spring 2026 schedule](https://cs231n.stanford.edu/schedule.html)

## Statistical learning theory and graphical-model inference

The official archived EECS545 syllabus includes learning theory and graphical-model topics beyond the currently detailed HMM/factor-graph introductions.

Status: still_missing

- [U-M EECS545 official archived syllabus](https://web.eecs.umich.edu/~honglak/teaching/eecs545/)
- [Probabilistic Machine Learning: An Introduction](https://probml.github.io/pml-book/book1.html)

## Complete CV geometry and SLAM coverage

CS231n is used for deep visual learning. Geometry, calibration and SLAM need their own stable courses or modules rather than being falsely attributed as a complete CS231n sequence.

Status: scope_boundary

- [Stanford CS231n Spring 2026 overview and prerequisites](https://cs231n.stanford.edu/)
- [Stanford CS231n Spring 2026 schedule](https://cs231n.stanford.edu/schedule.html)

## Theory-to-runtime integration

A mechanics derivation or a learned policy is insufficient without matching frames, action units, timestamps and hardware interfaces.

Status: expanded: new integration concepts; practical competence requires implementation and interface tests

- [MIT Missing Semester: shell, Git, debugging, builds, testing and CI](https://missing.csail.mit.edu/2020/)
- [MIT OCW: Effective Programming in C and C++](https://ocw.mit.edu/courses/6-s096-effective-programming-in-c-and-c-january-iap-2014/)
- [ROS 2 documentation source: official tutorials](https://github.com/ros2/ros2_documentation/tree/rolling/source/Tutorials)
- [ros2_control controller manager: lifecycle, limits and fallback](https://control.ros.org/rolling/doc/ros2_control/controller_manager/doc/userdoc.html)

## Sampling, filtering and delay

Existing timing nodes needed an explicit signal-processing prerequisite for aliasing, bandwidth and phase delay.

Status: expanded: new sampling/filtering concept; full frequency-domain analysis remains external course study

- [MIT OCW 6.003: Signals and Systems](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/)

## Contact transitions and physically valid motion

Rigid-body equations and friction alone do not explain discrete mode transitions or impact resets.

Status: expanded: hybrid modes added; full complementarity and nonsmooth analysis remain advanced extensions

- [MIT Underactuated Robotics notes](https://underactuated.mit.edu/)
- [MuJoCo mathematical and computational foundations](https://mujoco.readthedocs.io/en/stable/computation/)
- [MIT Robotic Manipulation: Perception, Planning, and Control](https://manipulation.mit.edu/)

## Grasp and wrench feasibility

An object pose or IK solution does not establish force closure or actuator-feasible manipulation.

Status: expanded: grasp map and closure concept; specialized dexterous-contact algorithms remain paper-level extensions

- [Modern Robotics: official book, software and chapter outline](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)
- [MIT Robotic Manipulation: Perception, Planning, and Control](https://manipulation.mit.edu/)

## Wheeled and mobile-robot foundations

The robot scope extends beyond humanoids and needs explicit nonholonomic wheel kinematics.

Status: expanded: differential-drive model; specialized wheel types and slip identification remain external extensions

- [Modern Robotics: official book, software and chapter outline](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)
- [MIT Visual Navigation: public lecture materials](https://vnav.mit.edu/lectures.html)

## Executable timed trajectories

Geometric planning and general trajectory optimization need a clear connection through time parameterization.

Status: expanded: time scaling added; full time-optimal path parameterization remains external study

- [Modern Robotics: official book, software and chapter outline](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)
- [MIT Underactuated Robotics notes](https://underactuated.mit.edu/)

## Estimation and SLAM beyond mechanics

Modern Robotics is not a comprehensive course in probabilistic filtering, nonlinear smoothing or visual-inertial navigation.

Status: existing nodes reused; dedicated estimation track added; no claim of complete estimator implementation

- [MIT Visual Navigation: public lecture materials](https://vnav.mit.edu/lectures.html)
- [MIT OCW 6.003: Signals and Systems](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/)

## Advanced control beyond basic robot feedback

Legged underactuation, Lyapunov methods, MPC and robust control need a deeper sequence after basic robot mechanics.

Status: existing concepts grouped into advanced control track; advanced robust/adaptive synthesis remains external depth

- [MIT Underactuated Robotics notes](https://underactuated.mit.edu/)
- [MIT OCW Underactuated Robotics](https://ocw.mit.edu/courses/6-832-underactuated-robotics-spring-2009/)

## Simulation fundamentals before engine comparisons

CSE598 simulation-associated papers do not replace numerical integration, importer, contact and sensor-loop foundations.

Status: dedicated foundation track; no assumption that reading an engine node proves working simulation

- [Drake Python tutorials](https://drake.mit.edu/)
- [MuJoCo mathematical and computational foundations](https://mujoco.readthedocs.io/en/stable/computation/)
- [MuJoCo modeling and compiler semantics](https://mujoco.readthedocs.io/en/stable/modeling.html)
- [Isaac Lab official how-to guides and concepts](https://isaac-sim.github.io/IsaacLab/main/source/how-to/index.html)

## Actuation and identification

A single URDF effort bound cannot model torque-speed limits, electrical dynamics, thermal restrictions or delay.

Status: expanded: actuator model added; exact motor/drive data and physical identification remain platform-specific

- [Modern Robotics: official book, software and chapter outline](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)
- [Isaac Lab official how-to guides and concepts](https://isaac-sim.github.io/IsaacLab/main/source/how-to/index.html)
- [MIT Underactuated Robotics notes](https://underactuated.mit.edu/)

## Scientific evidence and repeatability

Paper reading, deterministic code checks and real behavior evaluation establish different evidence scopes.

Status: expanded: replay and tests; learning outcomes are targets, not claims of learner mastery

- [MIT Missing Semester: shell, Git, debugging, builds, testing and CI](https://missing.csail.mit.edu/2020/)
- [ROS 2 rosbag2: official recording and playback software](https://github.com/ros2/rosbag2)
- [MIT Robotic Manipulation: Perception, Planning, and Control](https://manipulation.mit.edu/)

## Large-scale training and GPU efficiency

Robot researchers also need GPU memory, asynchronous execution and profiling, which are outside Modern Robotics.

Status: existing concepts mapped in explicit engineering modules; conceptual coverage is not an executed performance lab or working distributed-training run

- [Isaac Lab official how-to guides and concepts](https://isaac-sim.github.io/IsaacLab/main/source/how-to/index.html)
- [MIT Missing Semester: shell, Git, debugging, builds, testing and CI](https://missing.csail.mit.edu/2020/)
- [Stanford CS149: Parallel Computing — verified public course edition](https://gfxcourses.stanford.edu/cs149/fall25)
- [NVIDIA CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/)
- [PyTorch CUDA semantics](https://docs.pytorch.org/docs/stable/notes/cuda.html)
- [PyTorch distributed communication](https://docs.pytorch.org/docs/stable/distributed.html)

## Task-level reasoning and long-horizon autonomy

Local motion control does not by itself solve task composition, failures, memory and reasoning.

Status: partial existing coverage; formal task planning and behavior-tree/PDDL algorithms remain future expansion, not silently marked complete

- [MIT Robotic Manipulation: Perception, Planning, and Control](https://manipulation.mit.edu/)
- [MIT Underactuated Robotics notes](https://underactuated.mit.edu/)

## Hardware electronics and communication depth

Mechanical models and software APIs omit power integrity, embedded interfaces, drive electronics and detailed bus behavior.

Status: partial foundations only; a dedicated embedded/mechatronics course is still needed for hardware-design roles

- [MIT OCW: Effective Programming in C and C++](https://ocw.mit.edu/courses/6-s096-effective-programming-in-c-and-c-january-iap-2014/)
- [ROS 2 documentation source: official tutorials](https://github.com/ros2/ros2_documentation/tree/rolling/source/Tutorials)
- [ros2_control controller manager: lifecycle, limits and fallback](https://control.ros.org/rolling/doc/ros2_control/controller_manager/doc/userdoc.html)
