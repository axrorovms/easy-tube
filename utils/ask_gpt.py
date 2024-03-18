import g4f

def ask_gpt(prompt: str) -> str:
    print('bla bla bla')
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": prompt}],
    )
    return response
