from pathlib import Path
import subprocess,sys,shutil
p=Path(__file__).parent
subprocess.run([sys.executable,str(p/'source/build.py')],cwd=p/'source',check=True)
d=p/'docs';d.mkdir(exist_ok=True)
shutil.copy2(p/'source/dist/index.html',d/'index.html')
(d/'.nojekyll').write_text('')
(d/'data').mkdir(exist_ok=True)
shutil.copy2(p/'source/atlas.json',d/'data/atlas.json')
print('Built docs/index.html')
