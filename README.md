# Robotics Atlas

**Live website:** https://Leo-Haochen-Liu.github.io/robotics-atlas/

An interactive, source-linked robotics learning atlas. The current version contains 347 topics, 94 papers or official releases, and 1037 typed connections. World models remain one part of the wider robotics map.

## Use
Expand a category and then a branch, or search the Knowledge Library. Each concept includes LaTeX formulas, notation, definition, example, references and prerequisite/downstream networks. Each paper is one record with internal framework, training, evaluation, scale and limitations. The fixed arrow pad supports mobile panning without browser swipe gestures.

English is the default; the Chinese toggle shows Chinese titles and retained explanations. The page embeds its math renderer and figures, so it also works offline. External references require internet.

## Build
Run `python3 build_site.py`. Editable content and interface sources live in `source/`; the script generates the static `docs/` directory served by GitHub Pages. No API keys or external build services are needed.

## Evidence and coverage
This is a curated educational inventory, not an exhaustive list or popularity ranking. Primary references are attached to nodes. Official announcements are identified separately from full papers. Model-file counts apply to the pinned file and variant, not automatically to every physical robot. The atlas does not claim to have reproduced every method.

See [source attribution](SOURCES.md). Third-party research figures and KaTeX retain their source attribution and license terms.
