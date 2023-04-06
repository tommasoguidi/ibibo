from pathlib import Path
from tqdm import tqdm
import re


root = Path('lyrics')
_all_paths = list(root.rglob('*.txt'))
_n_paths = len(_all_paths)

# regex to match:
# 0. Deletes the files without section headers (e.g. [Intro], [Bridge]...)
# 1. Remove the '<Title> Lyrics' on top of each file
# 2. Replace the 'You might also like' with a newline
# 3. Remove the '<digit>Embed' at the end of the file
r0 = re.compile(r'\[')
r1 = re.compile(r'.*Lyrics')
r2 = re.compile(r'You might also like')
r3 = re.compile(r'[0-9]*Embed')

progress = tqdm(_all_paths, desc='Refining lyrics...', total=_n_paths)

deleted = 0
for path in progress:
    with open(path, mode='r', encoding='UTF-8') as f:
        _text = f.read()

    if re.search(r0, _text) is None:
        deleted += 1
        # print(f'Deleting {path}...')
        path.unlink()
    else:
        refined_text = re.sub(r1, r'', _text)
        refined_text = re.sub(r2, r'\n', refined_text)
        refined_text = re.sub(r3, r'', refined_text)

        with open(path, mode='w', encoding='UTF-8') as f:
            f.write(refined_text)

print(f'Process completed, {deleted} files were deleted.')
