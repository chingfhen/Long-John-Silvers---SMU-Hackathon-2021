from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
import yaml

with open(r"C:\Users\tanch\Documents\Coding Competitions\SMU\SMU HACKATHON 2021\config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

datastore = ElasticsearchDocumentStore(host="localhost", username="TA", password="123", index=config["index"], create_index =False, similarity = config['vector_similarity'])
