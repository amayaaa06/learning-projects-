from openai import OpenAI 
client = OpenAI(base_url = "http://127.0.0.1:8080", api_key="none")

completion = client.chat.completions.create(
    model='qwen2.5-1.5b', 
    messages=[
        {"role": "developer", "content": "you are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

print(completion.choices[0].message)

