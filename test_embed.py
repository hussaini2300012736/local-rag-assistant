import math
from foundry_local_sdk import Configuration, FoundryLocalManager

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b)

config = Configuration(app_name="rag_project")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

model = manager.catalog.get_model("qwen3-embedding-0.6b")
model.download()
model.load()

client = model.get_embedding_client()

sentences = [
    "The cat sat on the mat.",
    "A feline rested on the rug.",
    "The stock market crashed yesterday.",
]

vectors = [client.generate_embedding(s).data[0].embedding for s in sentences]

for i in range(1, len(sentences)):
    sim = cosine_similarity(vectors[0], vectors[i])
    print(f"Similarity between:\n  '{sentences[0]}'\n  '{sentences[i]}'\n  = {sim:.4f}\n")

model.unload()
