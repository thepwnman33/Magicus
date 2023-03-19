import os
from flask import Flask, jsonify, request, send_from_directory, render_template
from models_wrapper import CodeSnippet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Add CORS middleware to allow cross-origin requests
cors = CORS(app)

# Database configurations
DB_NAME = "mydatabase"
DB_USER = "your_new_user"
DB_PASSWORD = "qwerty"
DB_HOST = "localhost"
DB_PORT = "5432"

# Create a database engine and a session factory
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Session = sessionmaker(bind=engine)

# API endpoint to add a new code snippet
@app.route('/add_snippet', methods=['POST'])
def add_snippet():
    # Get the data from the request
    snippet_data = request.json

    # Create a session and add a new code snippet to the database
    session = Session()
    new_snippet = CodeSnippet(
        name=snippet_data['name'],
        description=snippet_data['description'],
        file_path=snippet_data['file_path'],
        code=snippet_data['code']
    )
    session.add(new_snippet)
    session.commit()

    # Return a success message
    return jsonify({'message': 'Code snippet added successfully.'})

# API endpoint to search code snippets
@app.route('/search', methods=['POST'])
def search_code_snippets():
    # Get search criteria from the request
    search_data = request.json

    # Create a session and query the database
    session = Session()
    query = session.query(CodeSnippet)

    # Apply search filters
    if 'name' in search_data:
        query = query.filter(CodeSnippet.name.contains(search_data['name']))
    if 'description' in search_data:
        query = query.filter(CodeSnippet.description.contains(search_data['description']))
    if 'code' in search_data:
        query = query.filter(CodeSnippet.code.contains(search_data['code']))

    # Fetch results and convert them to a list of dictionaries
    results = query.all()
    response_data = [{'id': result.id, 'name': result.name, 'description': result.description, 'file_path': result.file_path, 'code': result.code, 'latest_commit': result.latest_commit} for result in results]

    # Return JSON response
    return jsonify(response_data)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    input_text = data.get('input')
    code_snippet = CodeSnippet(input_text)
    code = code_snippet.generate_code()
    return jsonify({"code": code})

@app.route('/index1.html')
def index1():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'templates'), 'index1.html')


def run():
    app.run(debug=True, use_reloader=False)

# Run Flask app
if __name__ == '__main__':
    run()
