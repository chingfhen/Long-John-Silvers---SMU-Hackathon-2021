from haystack.preprocessor import PreProcessor
from haystack.schema import Document
import datetime

# converts "2020-11-23" in to python datetime - assumes "2020-11-23" is under ["tags"]["xxxxx_date"]
# assumes date is of the form YYYY-MM-DD
def add_datetime(document):   
    start_date = document['meta']["start_date"] 
    end_date = document['meta']["end_date"] 
    document['meta']["start_date"] = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    document['meta']["end_date"] = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    return document


# splits a document into smaller passages, no overlap - because long documents cannot be processed properly
def split_document(document: dict, num_words = 100, split_respect_sentence_boundary = True):

    if isinstance(document,Document):
        document = document.to_dict()
    
    if document['meta']["name"] == "summary":                                   # summaries will not be split
        return [document]
    
    pp = PreProcessor(split_by = "word",split_length  = num_words, split_overlap = 0, split_respect_sentence_boundary = split_respect_sentence_boundary)
    documents = [Document(**doc) for doc in pp.process(document)]

    return documents
	
    

	
