#importing the needed libraries
import sys 
import json
from openai import OpenAI 
from registry import TOOLS, FUNCS
from calendar_rag import search 

#creating a client that sends requests to the llama.cpp server
client = OpenAI(base_url="http://127.0.0.1:8080", api_key="none")

#system prompt 
SYSTEM = ("You answer questions about holidays and dates. Use the context provided "
          "with the question. For date calculations, call the tools. "
          "If you can't find the answer, say so.")

# gets the question (anything after chat.py)
question = " ".join(sys.argv[1:]) or input("Question: ")


context = "\n".join(f"- {text}" for score, text in search(question))


message = [
    {"role": "system", "content": SYSTEM },
    {"role": "user", "content": f"context:\n{context}\n\Question: {question}"},
] 


#tool loop 
while True:
    #sends the request
    msg = client.chat.completions.create(
        model="qwen2.5-1.5b", messages=message, tools=TOOLS).choices[0].message 
    message.append(msg)

    if not msg.tool_calls:
        print(msg.content)
        break 


    for call in msg.tool_calls:
        try:
            args = json.loads(call.function.arguments or "{}")
            result = FUNCS[call.function.name](**args)
        except Exeption as e:
            result = f"Error: {e}"
        message.append({"role": "tool", "tool_call_id": call.id,
                        "content": json.dumps(result, ensure_ascii=False, default= str)})

