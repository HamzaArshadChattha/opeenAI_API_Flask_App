from flask import Flask, render_template, request, jsonify
from openai_api.chatgpt_api import ChatGptBotAPI
from config import *

app = Flask(__name__)
chatgpt_api = ChatGptBotAPI(OPENAI_API_KEY)

@app.route('/')
def index():
    data = {
        'prompts': chatgpt_api.get_prompts()
    }
    return render_template('index.html', data=data)

@app.route('/create-prompt', methods=['POST'])
def create_prompt():
    """
    create a prompt message using the input received 
    from the user.
    """

    data = request.get_json()  # Extract the JSON data from the request
    text = data.get('text')    # Get the 'text' field from the JSON data
    # Do something with the submitted text (e.g., save it to a database)
    prompt = chatgpt_api.create_prompt(text)
    if prompt:
        result = {
            'status': 'success',
            'result': prompt}
        return jsonify(result), 200
    else:
        result = {
            'status': 'fail'
        }
        return jsonify(result), 400


@app.route('/delete-prompt/<item_id>', methods=['DELETE'])
def delete_prompt(item_id):
    """
    code to delete the item with the given ID
    Example: Delete item with ID from a database
    return some response
    """
    try:
        prompt_index = int(item_id)
        if chatgpt_api.delete_prompt(prompt_index):
            return jsonify({'message': f'Item with ID {item_id} deleted successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400

@app.route('/update-prompt/<item_id>', methods=['PUT'])
def update_prompt(item_id):
    """
    code to update the item with the given ID
    Example: Delete item with ID from a database
    return some response
    """
    try:
        prompt_index = int(item_id)
        data = request.get_json()
        text = data.get('text')
        updated_prompt = chatgpt_api.update_prompt(prompt_index, text)
        if updated_prompt:
            return jsonify({'result': updated_prompt, 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400

@app.route('/generate-response/<item_id>', methods=['GET'])
def generate_response(item_id):
    """
    code to generate the response for a prompt with the given ID
    Example: Delete item with ID from a database
    return some response
    """

    try:
        prompt_index = int(item_id)
        
        updated_prompt = chatgpt_api.get_response(prompt_index)
        if updated_prompt:
            return jsonify({'result': updated_prompt, 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400

if __name__ == '__main__':
    app.run()