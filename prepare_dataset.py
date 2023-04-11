import json
from pathlib import Path
from tqdm import tqdm
import re


root = Path('lyrics')
_all_paths = list(root.rglob('*.txt'))
_n_paths = len(_all_paths)

prompt_end_line = '\n\n###\n\n'
completion_end_line = ' END'

# the idea is to use each section of the song as the input prompt, while the whole song as the expected output
# kinda like a leave-one-out procedure
pattern = re.compile(r'\[')

lines = []
progress = tqdm(_all_paths, desc='Creating fine tuning examples...', total=_n_paths)
for path in progress:
    with open(path, mode='r', encoding='UTF-8') as f:
        _text = f.read()

    completion = f' {_text}{completion_end_line}'
    _result = re.finditer('\[', _text)
    _sections = [i.start() for i in _result]
    for i in range(len(_sections) - 1):
        _start = _sections[i]
        _end = _sections[i + 1]
        prompt = f'{_text[_start:_end]}{prompt_end_line}'
        line = {'prompt': prompt, 'completion': completion}
        lines.append(line)

with open("lyrics.jsonl", 'w', encoding='UTF-8') as f:
    for item in lines:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
