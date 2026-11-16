# Robotics Atlas

**Live website:** https://leo-haochen-liu.github.io/robotics-atlas/

An interactive, source-linked robotics learning atlas with **492 topics, 194 papers or releases, and 1527 typed connections**. World models remain part of the wider robotics map.

## Explore

Expand a category and branch, or search the Knowledge Library. Learning paradigms, model families, loss functions, training methods and application domains have separate homes. Classical models appear below neural and generative model families; only solid arrows state learning prerequisites. Dashed arrows distinguish usage, objectives, specialization and method connections. See [taxonomy conventions](TAXONOMY.md).

Each concept includes LaTeX, notation, a definition, example, references and prerequisite/downstream networks. Each paper is one record with internal framework, training, evaluation, scale and limitations. Both floating panels retain their title and close button while only the body scrolls. Direction buttons support mobile panning.

The CSE598 reading collection covers 20 topics and 106 reading entries. Browse it from the Knowledge Library or [the reading inventory](COURSE_READINGS.md). A scheduled reading association is separate from authorship and does not establish that a talk occurred.

English is the default; the Chinese toggle shows Chinese titles and retained explanations. The page embeds its math renderer and figures and can work offline. External references require internet.

## Build

Run `python3 build_site.py`. Editable data and interface sources live in `source/`; the script builds `docs/` for GitHub Pages and updates paper/course inventories. No API key or external build service is required.

## Evidence and coverage

This is a curated educational inventory, not an exhaustive list or popularity ranking. Each node links primary sources. Official releases are identified separately from full papers. Robot-file counts apply to the pinned model and variant; they are not hardware performance measurements. The atlas does not claim independent reproduction of every method.

See [paper inventory](PAPER_INVENTORY.md) and [source attribution](SOURCES.md). Third-party research figures and KaTeX retain their source attribution and license terms.
