import json
import ollama
import re
from sentence_transformers import SentenceTransformer
from config.environment import OLLAMA_HOST, OLLAMA_MODEL, SENTENCE_TRANSFORMER_MODEL, OPENROUTER_API_URL, OPENROUTER_API_KEY, OPENROUTER_MODEL
from openai import OpenAI

def perform_rag(connection, user_input, type):
    # Initialize the SentenceTransformer model
    model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
    # Perform document retrieval
    retrieved_docs = search_document(connection, user_input, model)
    # Create the prompt with the retrieved documents
    context = "\n".join([doc['doc'] for doc in retrieved_docs])
    prompt = f"Context: {context}\n\nQuestion: {user_input}\nAnswer:"
    if type == 'ollama':
      # Get the response from Ollama
      return chat_with_ollama(prompt)
    elif type == 'openrouter':
      # Get the response from OpenRouter
      return chat_with_open_router(prompt)

def chat_with_ollama(prompt):
    llm_agent = ollama.Client(host=OLLAMA_HOST)
    response = llm_agent.chat(model=OLLAMA_MODEL, messages=[
        {
            "role": "user", 
            "content": prompt
        }
    ])
    # return response
    content = response['message']['content']
    return remove_thinking(content)

def chat_with_open_router(prompt):
    client = OpenAI(
      base_url=OPENROUTER_API_URL,
      api_key=OPENROUTER_API_KEY,
    )
    completion = client.chat.completions.create(
      extra_headers={},
      extra_body={},
      model=OPENROUTER_MODEL,
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt
            }
          ]
        }
      ]
    )
    # print(completion)
    return completion.choices[0].message.content

def remove_thinking(text):
  # Regular expression to remove <think> tags and their content
  cleaned_content = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
  # Strip any extra whitespace
  cleaned_content = cleaned_content.strip()
  return cleaned_content

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