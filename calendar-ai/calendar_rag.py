# importing the needed libraries 
import json
import numpy as np
import openai

# creates a client to send requests to the local server 
emb = openai.OpenAI(base_url="http://127.0.0.1:8081/v1", api_key="x")


# embeds the texts and normalize them 
def embed(texts):
    out = []
    for i in range(0, len(texts), 16):  # small batches
        r = emb.embeddings.create(model="x", input=texts[i:i+16])
        out += [d.embedding for d in r.data]
    v = np.array(out)
    return v / np.linalg.norm(v, axis=1, keepdims=True)

# reads the file 
entries = json.load(open("holidays.json", encoding="utf-8"))

# gives the values for each text 
texts = [e["text"] for e in entries]

# calls the embed (sends sentences to the server and gets back vectors)
vectors = embed(["title: none | text: " + t for t in texts])


# embeds the questions and compares them with the vector datas and gives the best ones 
def search(question, k=5):

    q = embed(["task: search result | query: " + question])[0]
    scores = vectors @ q
    best = np.argsort(scores)[::-1][:k]
    return [(float(scores[i]), texts[i]) for i in best]
