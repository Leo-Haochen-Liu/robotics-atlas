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
cur=j['curriculum']
clines=['# Foundation curriculum','',cur['maintenance']['foundations'],'','These are course-anchored editorial modules. Source-backed topics, optional extensions and atlas supplements are distinguished in their records. A module mapping does not claim that the atlas reproduces the entire course.','']
for course in cur['courses']:
    clines+=['## '+course['title'],'',course['scope'],'']
    for src in course['source_urls']:clines.append('- ['+src['title']+']('+src['url']+')')
    clines+=['','Modules: '+ '; '.join(m['title'] for m in course['modules'])+'.','']
(p/'CURRICULUM.md').write_text('\n'.join(clines))
lines=['# Curriculum coverage audit','','An audit of learning references and remaining lesson depth, not a certification of competence or a claim of an exhaustive curriculum.\n','Framework references: [CMU robotics curriculum](https://www.ri.cmu.edu/education/academic-programs/master-of-science-robotics/curriculum/), [Stanford robot autonomy](https://bulletin.stanford.edu/courses/2185453).','']
for gap in cur['gaps']:
    lines+=['## '+gap.get('title',gap.get('topic','Coverage note')),'',str(gap.get('why',gap.get('reason',gap.get('note','')))),'','Status: '+str(gap.get('coverage_status',gap.get('status','Reference / scope note'))),'']
    for src in gap.get('course_sources',gap.get('source_urls',[])):lines.append('- ['+src['title']+']('+src['url']+')')
    lines+=['']
(p/'COVERAGE_AUDIT.md').write_text('\n'.join(lines))
(p/'README.md').write_text(f'''# Robotics Atlas

**Live website:** https://leo-haochen-liu.github.io/robotics-atlas/

An interactive, source-linked robotics learning atlas with **{len(j['nodes'])} canonical topics, {len(papers)} papers or releases, and {len(j['edges'])} typed connections**.

## Foundations and Research

**Foundations** uses stable course anchors: SI602/ROB501 and mathematics bridges, Modern Robotics, EECS545, Berkeley CS285, Stanford CS231n, U-M CSE598 Action and Perception, a simulation foundation track, and engineering/research practice. The current {len(cur['courses'])} course tracks map {cur['coverage']['mapped_foundation_nodes']} concept records into modules. Advanced control, estimation, manipulation and systems sources supplement the named core courses. See [curriculum and sources](CURRICULUM.md).

**Research** organizes papers and reusable methods in {len(cur['topics'])} topic collections. Robot Soccer is one collection containing ball perception, contact, skills, robot platforms and papers. World models, VLA, motion, manipulation, geometry/SLAM, representations, simulation and reliability remain available. Every displayed reference points to one canonical record. A concept can be referenced by several courses or research topics without duplicating its definition.

Paper pages link to their required concepts. Concept pages show relevant papers and course modules, so a method such as behavior cloning or conditional flow matching is close to the research that uses it. The {len(sessions)}-topic CSE598 collection retains {len(readings)} reading associations.

Use the two buttons at the top to switch maps. Both floating panels keep their titles and close buttons visible while their bodies scroll. Zoom and directional buttons support mobile viewing. English is the default, with a Chinese toggle. LaTeX and figures are embedded for offline reading; external sources require internet.

## Coverage and maintenance

The [coverage audit](COVERAGE_AUDIT.md) identifies additions, mappings and remaining study depth. A concept entry is not equivalent to a complete university course, executed lab or hardware skill. This is a curated learning framework, not an exhaustive or popularity-ranked inventory. The underlying [typed taxonomy](TAXONOMY.md) remains descriptive metadata rather than the main browsing hierarchy.

Stable curriculum records live in `source/curriculum_*.json`; reviewed supplemental assignments are pinned in `source/foundation_supplements.json`. Adding a research paper does not automatically alter course modules. Paper records remain in the expansion data; topic links are built separately by `source/curriculum_build.py`. No automatic update schedule is configured.

Run `python3 build_site.py` to generate `docs/` for GitHub Pages and refresh the public inventories. No API key is required.

See [paper inventory](PAPER_INVENTORY.md), [course readings](COURSE_READINGS.md), and [source attribution](SOURCES.md). Third-party research figures and KaTeX retain their attribution and license terms.
''')
print('Built site, curriculum and coverage inventories')
