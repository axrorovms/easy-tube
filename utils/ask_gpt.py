from openai import OpenAI
from data import config

import time

client = OpenAI(api_key=config.GPT_API_KEY)


def gpt(txt: str, lang: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"Summarize content, you are provided ONLY with crucial points not as a article. Answer in {lang}. At least 50 words!"
            },
            {
                "role": "user",
                "content": txt
            }
        ],

    )

    if response:
        print(response)
        return response.choices[0].message.content
    else:
        return "Sorry, unable to get a response within the specified time."
