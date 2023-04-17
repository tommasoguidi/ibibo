import json
from pathlib import Path
from tqdm import tqdm
import re
import numpy as np


root = Path('lyrics')
_all_paths = list(root.rglob('*.txt'))
_n_paths = len(_all_paths)
tiny = True

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

print(f'{len(lines)} examples in the dataset.')
if tiny:
    chance = np.random.rand(len(lines))
    tiny_lines = []
    for i,j in zip(lines, chance):
        if j <= 0.01:
            tiny_lines.append(i)
    print(f'{len(tiny_lines)} examples in the tiny dataset.')
    with open("tiny_lyrics.jsonl", mode='w', encoding='UTF-8') as f:
        for item in tiny_lines:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
else:
    with open("lyrics.jsonl", mode='w', encoding='UTF-8') as f:
        for item in lines:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
