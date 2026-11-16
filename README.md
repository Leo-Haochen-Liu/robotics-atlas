# Robotics Atlas

**Live website:** https://leo-haochen-liu.github.io/robotics-atlas/

An interactive, source-linked robotics learning atlas with **524 canonical topics, 194 papers or releases, and 1631 typed connections**.

## Foundations and Research

**Foundations** uses stable course anchors: SI602/ROB501 and mathematics bridges, Modern Robotics, EECS545, Berkeley CS285, Stanford CS231n, U-M CSE598 Action and Perception, a simulation foundation track, and engineering/research practice. The current 14 course tracks map 330 concept records into modules. Advanced control, estimation, manipulation and systems sources supplement the named core courses. See [curriculum and sources](CURRICULUM.md).

**Research** organizes papers and reusable methods in 9 topic collections. Robot Soccer is one collection containing ball perception, contact, skills, robot platforms and papers. World models, VLA, motion, manipulation, geometry/SLAM, representations, simulation and reliability remain available. Every displayed reference points to one canonical record. A concept can be referenced by several courses or research topics without duplicating its definition.

Paper pages link to their required concepts. Concept pages show relevant papers and course modules, so a method such as behavior cloning or conditional flow matching is close to the research that uses it. The 20-topic CSE598 collection retains 106 reading associations.

Use the two buttons at the top to switch maps. Both floating panels keep their titles and close buttons visible while their bodies scroll. Zoom and directional buttons support mobile viewing. English is the default, with a Chinese toggle. LaTeX and figures are embedded for offline reading; external sources require internet.

## Coverage and maintenance

The [coverage audit](COVERAGE_AUDIT.md) identifies additions, mappings and remaining study depth. A concept entry is not equivalent to a complete university course, executed lab or hardware skill. This is a curated learning framework, not an exhaustive or popularity-ranked inventory. The underlying [typed taxonomy](TAXONOMY.md) remains descriptive metadata rather than the main browsing hierarchy.

Stable curriculum records live in `source/curriculum_*.json`; reviewed supplemental assignments are pinned in `source/foundation_supplements.json`. Adding a research paper does not automatically alter course modules. Paper records remain in the expansion data; topic links are built separately by `source/curriculum_build.py`. No automatic update schedule is configured.

Run `python3 build_site.py` to generate `docs/` for GitHub Pages and refresh the public inventories. No API key is required.

See [paper inventory](PAPER_INVENTORY.md), [course readings](COURSE_READINGS.md), and [source attribution](SOURCES.md). Third-party research figures and KaTeX retain their attribution and license terms.
