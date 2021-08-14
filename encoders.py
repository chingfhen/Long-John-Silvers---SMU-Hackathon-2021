from sentence_transformers import SentenceTransformer, CrossEncoder
import yaml

with open(r"C:\Users\tanch\Documents\Coding Competitions\SMU\SMU HACKATHON 2021\config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    
bi_encoder = SentenceTransformer(config["bi_encoder"])
bi_encoder.max_seq_length = 200
cross_encoder = CrossEncoder(config["cross_encoder"])

	
def embed_documents(documents):
    if isinstance(documents,dict):
        documents = [documents]
        
    embeddings = bi_encoder.encode([d['text'] for d in documents])
    for i,d in enumerate(documents):
        d["embedding"] = embeddings[i]
    return documents
    
    