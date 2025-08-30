from flask import Flask, render_template, request, jsonify
from config import database
from services.chat import chat_with_ollama
import knowledge_embedding

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    user_input_lower = str(user_input).lower()
    db = database.Database()
    connection = db.get_connection()
    response = chat_with_ollama(connection, user_input_lower)
    db.close_connection(connection)

    if response.status_code == 200:
        data = response.json()
        return jsonify({'response': data.get('response', 'No response from model')})
    else:
        return jsonify({'error': 'Failed to get response from model'}), 500
    
@app.route('/embedding', methods=['GET'])
def embedding():
    knowledge_embedding.run_embedding()
    return "Knowledge embedding process completed."

if __name__ == '__main__':
    app.run(debug=True)
