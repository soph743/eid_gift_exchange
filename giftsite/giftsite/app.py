from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_text():
    data = request.json
    name = data.get("text", "")

    try:
        with open("data/results.txt", "r") as file:
            content = file.read()
        if name in content:
            return jsonify({"message"})
        else:
            return jsonify({"message"})
    except FileNotFoundError:
        return jsonify({"error": "File not found!"}), 404

@app.route('/read', methods=['GET'])
def read_text():
    try:
        with open("data/results.txt", "r") as file:
            content = file.read()
        names = content.split()
        random_name = random.choice(names) if names else None
        name_to_remove = random_name
        updated_content = content.replace(name_to_remove, "")
        with open("data/results.txt", "w") as file:
            file.write(updated_content)
        return jsonify({"content": content, "you_will_give_a_gift_to": random_name})
    except FileNotFoundError:
        return jsonify({"error": "File not found!"}), 404

@app.route('/remove', methods=['POST'])
def remove_text():
    data = request.json
    name_to_remove = data.get("text", "")

    try:
        with open("data/results.txt", "r") as file:
            content = file.read()

        if name_to_remove in content:
            updated_content = content.replace(name_to_remove, "")
            with open("data/results.txt", "w") as file:
                file.write(updated_content)
            return jsonify({"message"})
        else:
            return jsonify({"message"})
    except FileNotFoundError:
        return jsonify({"error": "File not found!"}), 404


if __name__ == '__main__':
    app.run(debug=True)
