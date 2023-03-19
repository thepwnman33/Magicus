# client.py
import requests
import json

def get_formatted_code_snippet(snippet_name):
    # Replace the following with your actual API endpoint
    url = "http://localhost:5000/search"
    data = {"name": snippet_name}

    response = requests.post(url, json=data)
    response_json = response.json()

    code_snippet = response_json[0]['code']
    formatted_code = code_snippet.replace('\\n', '\n')
    return formatted_code

if __name__ == "__main__":
    snippet_name = "test1.py"
    formatted_code = get_formatted_code_snippet(snippet_name)
    print(formatted_code)
