from openai import OpenAI
from data import config
client = OpenAI(api_key=config.GPT_API_KEY)

def gpt(txt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Summarize content you are provided with crucial points."
            },
            {
                "role": "user",
                "content": txt
            }
        ],
        temperature=0.7,
        max_tokens=64,
        top_p=1
    )

    return response.choices[0].message.content
