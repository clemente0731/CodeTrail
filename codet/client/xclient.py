import os
from openai import OpenAI


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ['NVIDIA_API_KEY']
)

preliminary_prompt = "where is a bunch of git diff.you are the absolute expert of the entire project. Please help me analyze it:"
diff = "some code diff"
full_prompt = preliminary_prompt + diff

completion = client.chat.completions.create(
    model="meta/llama-3.1-405b-instruct",
    messages=[{"role": "user", "content": full_prompt}],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=True
)