# Sources and third-party resources

- Vaswani et al., Attention Is All You Need, https://arxiv.org/html/1706.03762 . Original Figures 1 and 2 are attributed in the interface. The paper grants figure reproduction for journalistic or scholarly use with attribution. Highlight overlays and teaching redraws are additions for this educational atlas.
- ID-WM original paper and appendix: https://arxiv.org/html/2610.42146v1 . Method dataflow redraw is labeled as teaching material.
- KaTeX 0.19.1: https://katex.org/docs/browser . Vendored from the official npm package, under MIT license (vendor/katex/LICENSE).
- Primary textbooks and original research references remain attached to each topic.

Mathematical architecture variant: the canonical Transformer node formula and the original-paper context diagram use post-norm. Modern pre-norm variants are mentioned as alternatives, not conflated with that diagram.

## Robot description audits

Robot records use official [Unitree model descriptions](https://github.com/unitreerobotics/unitree_ros) and [Booster robot assets](https://github.com/BoosterRobotics/booster_assets). Each record links its exact commit and URDF path. Joint counts, declared mass sums, link counts and selected numerical limits were parsed from those XML files on 2026-11-16; seven source hashes were independently rechecked. No manufacturer mesh files are redistributed. File validation does not establish simulator correctness or physical hardware performance.

All new perception, software, motion and soccer topics attach their primary references directly to their nodes. Ambiguous remembered names remain recorded as unresolved names rather than being assigned to unrelated papers.

## Classification and course readings

The typed browsing taxonomy distinguishes learning paradigms, models, objective functions, fitting/transfer methods, application domains and system families. [EECS545](https://web.eecs.umich.edu/~honglak/teaching/eecs545/) and the primary textbooks linked at each node inform the organization; it is an editorial learning structure. The CSE598 collection publishes paper references and professional presenter associations, with reading context distinguished from authorship and talk delivery. Private course files, meeting logistics and learning progress are excluded.
