from sentence_transformers import SentenceTransformer
import json
from elasticsearch import Elasticsearch
from llama_cpp import Llama

# Initialize Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the LLaMA model
def load_llm_model(model_path):
    """Load the LLaMA model from the specified path."""
    try:
        llm = Llama(
            model_path=model_path,
            # Configure other parameters if needed
        )
        return llm
    except Exception as e:
        print(f"Failed to load LLaMA model: {e}")
        return None

def generate_sentence_embeddings(texts):
    embeddings = model.encode(texts)
    return embeddings.tolist()

def create_index(es, index_name):
    settings = {
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "question": {"type": "text"},
                "answer": {"type": "text"},
                "vector": {"type": "dense_vector", "dims": 384}  # Use the correct dimension based on model
            }
        }
    }
    es.indices.create(index=index_name, body=settings)
    print(f"Index '{index_name}' created successfully.")

def push_data_with_embeddings(es, index_name, data):
    texts = [item['question'] + " " + item['answer'] for item in data]
    embeddings = generate_sentence_embeddings(texts)
    
    for i, item in enumerate(data):
        item['vector'] = embeddings[i]  # Add embedding to document
        doc_id = f"doc_{i}"
        es.index(index=index_name, id=doc_id, body=item)
        print(f"Document {doc_id} indexed with embedding.")

def search_es(query_vector, es_host='http://localhost:9200', index_name='itops_sbert'):
    es = Elasticsearch([es_host])
    search_query = {
        "size": 2,  # Number of results to return
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {
                        "query_vector": query_vector
                    }
                }
            }
        }
    }
    response = es.search(index=index_name, body=search_query)
    search_results = response['hits']['hits']
    results = []
    for hit in search_results:
        results.append(hit['_source']['answer'])
    return results

def rag_system(user_input, es, index_name, llm, max_tokens=300):
    # Generate embedding for the user's input
    query_embedding = generate_sentence_embeddings([user_input])[0]
    
    # Retrieve relevant information from ElasticSearch
    search_results = search_es(query_embedding, es_host='http://localhost:9200', index_name=index_name)
    
    # Combine retrieved information into a context for the LLM
    context = " ".join(search_results)
    prompt = f"Reply to this message: '{user_input}' of the user, using this information: '{context}'. Your response should be to the point and shouldnt be anything apart from the this information: '{context}'. This is a strict RULE DONT BREAK IT"
    
    print("\nPrompt sent to LLM:\n" + prompt + "\n")

    # Get the response from the LLM
    try:
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": "You are an expert IT Operation professional, who has a lot of experience in Enterprise Marketing Management Tools like Unica, Oracle. You are also highly skilled in Linux."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.35,
            max_tokens=max_tokens
        )

        # Print the entire response for debugging
        print(f"Full LLM Response: {response}")

        # Extract and print just the 'content' part (the answer)
        response_text = response['choices'][0]['message']['content']
        print(f"Answer: {response_text}")
        
        return response_text.strip()
    except Exception as e:
        print(f"Error during LLM inference: {e}")
        return "Error generating response."


if __name__ == "__main__":
    es_host = 'http://localhost:9200'
    es = Elasticsearch([es_host])

    # Define the path to your LLaMA model
    llm_model_path = './models/meta-llama-3.1-8b-instruct-q6_k.gguf'

    # Load the LLaMA model
    llm = load_llm_model(llm_model_path)
    if not llm:
        print("LLaMA model could not be loaded. Exiting.")
        exit(1)
    
    index_name = "itops_sbert"

    print("RAG system is ready! Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            print("LLama-3: Goodbye!")
            break

        # Get the response from the RAG system
        response = rag_system(user_input, es, index_name, llm)
        print(f"LLama-3: {response}")
