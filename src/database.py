import os
import json
import chromadb
from chromadb.utils import embedding_functions

def get_chroma_client():
    return chromadb.PersistentClient(path="./chroma_db")

def setup_and_populate_db(json_file_path="./data/sports_facts.json"):
   
    client = get_chroma_client()

    
    
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    
    collection = client.get_or_create_collection(
        name="sports_history",
        embedding_function=embedding_fn
    )

    
    if collection.count() > 0:
        print(f"Database already populated with {collection.count()} facts.")
        return collection

    
    if not os.path.exists(json_file_path):
        print(f"Error: Raw fact data file not found at {json_file_path}")
        return collection

    
    with open(json_file_path, "r") as f:
        try:
            facts_list = json.load(f)
        except json.JSONDecodeError:
            facts_list = []

    documents = []
    metadata_list = []
    ids = []

    for idx, item in enumerate(facts_list):
        documents.append(item["fact"])
        
        metadata_list.append({"sport": item["sport"]})
        ids.append(f"fact_{idx}")

    if documents:
        collection.add(
            documents=documents,
            metadatas=metadata_list,
            ids=ids
        )
    print(f"Successfully vectorized and stored {len(documents)} facts.")
    return collection

def query_historic_facts(sport, query_text, n_results=2):
   
    client = get_chroma_client()
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(
        name="sports_history",
        embedding_function=embedding_fn
    )

    results = collection.query(
        query_texts=[query_text],
        n_results=10,
        where={"sport": sport}
    )

    documents = results.get("documents", [[]])[0]
    
    import random
    if len(documents) > n_results:
        return random.sample(documents, n_results)
    return documents

def bulk_add_facts_to_db(new_facts, json_file_path="./data/sports_facts.json"):
    client = get_chroma_client()
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(
        name="sports_history",
        embedding_function=embedding_fn
    )

    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as f:
            try:
                existing_facts = json.load(f)
            except json.JSONDecodeError:
                existing_facts = []
    else:
        existing_facts = []

    current_count = len(existing_facts)
    existing_facts.extend(new_facts)

    with open(json_file_path, "w") as f:
        json.dump(existing_facts, f, indent=4)

    documents = []
    metadata_list = []
    ids = []

    for idx, item in enumerate(new_facts):
        documents.append(item["fact"])
        metadata_list.append({"sport": item["sport"]})
        ids.append(f"fact_{current_count + idx}")

    if documents:
        collection.add(
            documents=documents,
            metadatas=metadata_list,
            ids=ids
        )
    return len(documents)