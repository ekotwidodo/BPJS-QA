import json
import pandas as pd
from config import database
from sentence_transformers import SentenceTransformer
from config.environment import SENTENCE_TRANSFORMER_MODEL

def run_embedding():
  # create instance of the embedding model
  model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
  db = database.Database()
  connection = db.get_connection()
  # read the CSV file into a pandas DataFrame
  df = pd.read_csv('data/bpjs_kb.csv')

  # iterate over each row in the DataFrame
  for index, row in df.iterrows():
    doc = str(row['question']) + " " + str(row['answer']) + " " + str(row['source'])
    try:
      # generate the embedding for the document
      embedding = model.encode(doc).tolist()
      # convert the embedding to a JSON string
      embedding_json = json.dumps(embedding)
      # prepare the SQL query to insert the document and its embedding into the database
      sql = "INSERT INTO documents (doc, embedding) VALUES (%s, %s)"
      val = (doc, embedding_json)
      # execute the SQL query
      cursor = connection.cursor()
      cursor.execute(sql, val)
      connection.commit()
      cursor.close()
      print(f"Inserted row {index} with ID {cursor.lastrowid}")
    except Exception as e:
      print(f"Error inserting row {index}: {e}")
  
  db.close_connection(connection)


