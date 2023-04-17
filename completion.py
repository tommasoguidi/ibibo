import openai
from pathlib import Path
from secret_keys import OPENAI_API_KEY, CURIE_FINE_TUNED_MODEL, DAVINCI_FINE_TUNED_MODEL
import os


PROMPT_END_LINE = '\n\n###\n\n'
COMPLETION_END_LINE = ' END'
T = 0.4
N = 3
FREQUENCY_PENALTY = 0.6

examples_dir = Path('examples')
ex = 'Ex5'
tiny = True
if tiny:
    FINE_TUNED_MODEL = DAVINCI_FINE_TUNED_MODEL
    completions_dir = Path('davinci_completions') / ex
else:
    FINE_TUNED_MODEL = CURIE_FINE_TUNED_MODEL
    completions_dir = Path('completions') / ex

if not os.path.isdir(completions_dir):
    os.mkdir(completions_dir)
ex_path = examples_dir / (ex + '.txt')

with open(ex_path, encoding='UTF-8', mode='r') as f:
    text = f.read()

MY_PROMPT = text + PROMPT_END_LINE
MAX_TOKENS = 2048 - len(MY_PROMPT)

openai.api_key = OPENAI_API_KEY
response = openai.Completion.create(
           model=FINE_TUNED_MODEL,
           prompt=MY_PROMPT,
           stop=[COMPLETION_END_LINE],
           temperature=T,
           n=N,
           max_tokens=MAX_TOKENS,
           frequency_penalty=FREQUENCY_PENALTY
           )

for choice in response['choices']:
    index = choice['index']
    text = choice['text']
    if FREQUENCY_PENALTY:
        f_name = f'{ex}_temp={str(T)}_freq={FREQUENCY_PENALTY}_{index}.txt'
    else:
        f_name = f'{ex}_temp={str(T)}_{index}.txt'
    compl_path = completions_dir / f_name

    with open(compl_path, mode='w', encoding='UTF-8') as f:
        f.write(text)
