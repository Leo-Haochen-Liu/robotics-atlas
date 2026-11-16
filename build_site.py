"""Build the standalone site and regenerate its public content inventories."""
from pathlib import Path
import subprocess,sys,shutil,json
p=Path(__file__).parent
subprocess.run([sys.executable,str(p/'source/build.py')],cwd=p/'source',check=True)
d=p/'docs';d.mkdir(exist_ok=True)
shutil.copy2(p/'source/dist/index.html',d/'index.html')
(d/'.nojekyll').write_text('')
(d/'data').mkdir(exist_ok=True)
shutil.copy2(p/'source/atlas.json',d/'data/atlas.json')
j=json.loads((d/'data/atlas.json').read_text());papers=[n for n in j['nodes'] if n['kind']=='paper'];roots=sum(not x['parent'] for x in j['taxonomy'].values())
lines=['# Robotics paper inventory','',f"Checked: {j['coverage']['checked_date']}. Curated and expandable; not an exhaustive survey.",'','| Branch | Paper / official release | Date | Primary reference |','| --- | --- | --- | --- |']
for n in sorted(papers,key=lambda n:(n['group'],n['en'].lower())):
    src=n['sources'][0]
    lines.append('| '+' | '.join([j['taxonomy'][n['group']]['en'],n['en'].replace('|','/'),str(n['paper'].get('date','See source')).replace('|','/'),'[Source]('+src['url']+')'])+' |')
(p/'PAPER_INVENTORY.md').write_text('\n'.join(lines)+'\n')
c=j.get('course598',{});sessions=c.get('sessions',[]);readings=[r for s in sessions for r in s['readings']]
if sessions:
    lines=['# CSE598: Action and Perception reading collection','',c['scope'],'','Public course source: '+c['public_course_url'],'']
    for s in sessions:
        lines+=['## '+s['topic'],'','Associated presenters: '+', '.join(x['name'] for x in s['speakers'])+'.','']
        for r in s['readings']:
            lines.append(('- ['+r['title']+']('+r['url']+')' if r.get('url') else '- '+r['title'])+(' — [Atlas node](https://leo-haochen-liu.github.io/robotics-atlas/#'+r['node_id']+')' if r.get('node_id') else ' — exact record unresolved'))
        if s.get('unresolved_reading'):lines+=['','Unresolved: '+s['unresolved_reading']['term']+' — '+s['unresolved_reading']['reason']]
        lines+=['']
    (p/'COURSE_READINGS.md').write_text('\n'.join(lines))
(p/'README.md').write_text(f'''# Robotics Atlas

**Live website:** https://leo-haochen-liu.github.io/robotics-atlas/

An interactive, source-linked robotics learning atlas with **{len(j['nodes'])} topics, {len(papers)} papers or releases, and {len(j['edges'])} typed connections**. World models remain part of the wider robotics map.

## Explore

Expand a category and branch, or search the Knowledge Library. Learning paradigms, model families, loss functions, training methods and application domains have separate homes. Classical models appear below neural and generative model families; only solid arrows state learning prerequisites. Dashed arrows distinguish usage, objectives, specialization and method connections. See [taxonomy conventions](TAXONOMY.md).

Each concept includes LaTeX, notation, a definition, example, references and prerequisite/downstream networks. Each paper is one record with internal framework, training, evaluation, scale and limitations. Both floating panels retain their title and close button while only the body scrolls. Direction buttons support mobile panning.

The CSE598 reading collection covers {len(sessions)} topics and {len(readings)} reading entries. Browse it from the Knowledge Library or [the reading inventory](COURSE_READINGS.md). A scheduled reading association is separate from authorship and does not establish that a talk occurred.

English is the default; the Chinese toggle shows Chinese titles and retained explanations. The page embeds its math renderer and figures and can work offline. External references require internet.

## Build

Run `python3 build_site.py`. Editable data and interface sources live in `source/`; the script builds `docs/` for GitHub Pages and updates paper/course inventories. No API key or external build service is required.

## Evidence and coverage

This is a curated educational inventory, not an exhaustive list or popularity ranking. Each node links primary sources. Official releases are identified separately from full papers. Robot-file counts apply to the pinned model and variant; they are not hardware performance measurements. The atlas does not claim independent reproduction of every method.

See [paper inventory](PAPER_INVENTORY.md) and [source attribution](SOURCES.md). Third-party research figures and KaTeX retain their source attribution and license terms.
''')
print('Built docs/index.html and content inventories')
