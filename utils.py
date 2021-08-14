import json
import yaml

# reads json file
def read_document(path):
    with open(path) as f:
        document = json.load(f)
    return document
            
