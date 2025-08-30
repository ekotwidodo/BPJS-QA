import json
import ollama
from sentence_transformers import SentenceTransformer
from config.environment import OLLAMA_HOST, OLLAMA_MODEL, SENTENCE_TRANSFORMER_MODEL

def chat_with_ollama(connection, user_input):
    llm_agent = ollama.Client(host=OLLAMA_HOST)
    model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
    retrieved_docs = search_document(connection, user_input, model)
    context = "\n".join([doc['doc'] for doc in retrieved_docs])
    prompt = f"Context: {context}\n\nQuestion: {user_input}\nAnswer:"
    response = llm_agent.chat(model=OLLAMA_MODEL, messages=[
        {
            "role": "user", 
            "content": prompt
        }
    ])
    # return response
    return response['message']['content']

def search_document(connection, query, model, top_k=5):
  results = []
  try:
    # generate the embedding for the query
    query_embedding = model.encode(query).tolist()
    query_embedding_json = json.dumps(query_embedding)

    # prepare the SQL query to find the most similar documents
    sql = """
      SELECT doc, vec_cosine_distance(embedding, %s) AS similarity
      FROM documents
      ORDER BY similarity ASC
      LIMIT %s;
    """
    val = (query_embedding_json, top_k)

    # execute the SQL query
    cursor = connection.cursor()
    cursor.execute(sql, val)
    query_results = cursor.fetchall()
    connection.commit()
    cursor.close()

    for result in query_results:
      doc, similarity = result
      results.append({"doc": doc, "similarity": similarity})

    return results
  except Exception as e:
    print(f"Error searching documents: {e}")