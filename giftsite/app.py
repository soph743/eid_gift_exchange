from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_text():
    data = request.json
    input_name = data.get("text", "").strip()

    try:
        with open("giftsite/data/results.txt", "r") as file:
            names = file.read().splitlines()  # Read names line by line

        if input_name in names:
            return jsonify({"message": f"{input_name} is in the list."})
        else:
            return jsonify({"message": f"{input_name} is NOT in the list."})
    except FileNotFoundError:
        return jsonify({"error": "File not found!"}), 404

@app.route('/read', methods=['POST'])
def read_text():
    data = request.json
    input_name = data.get("text", "").strip()

    try:
        with open("giftsite/data/results.txt", "r") as file:
            names = file.read().splitlines()

        if not names:
            return jsonify({"error": "No names available!"}), 400

        # Ensure the random name is not the same as the input name
        available_names = [name for name in names if name != input_name]
        if not available_names:
            return jsonify({"error": "No available names left!"}), 400

        random_name = random.choice(available_names)

        # Remove selected name from file
        updated_names = [name for name in names if name != random_name]
        with open("giftsite/data/results.txt", "w") as file:
            file.write("\n".join(updated_names))

        return jsonify({"you_will_give_a_gift_to": random_name})

    except FileNotFoundError:
        return jsonify({"error": "File not found!"}), 404

@app.route('/remove', methods=['POST'])
def remove_text():
    data = request.json
    name_to_remove = data.get("text", "").strip()

    try:
        with open("giftsite/data/results.txt", "r") as file:
            names = file.read().splitlines()

        if name_to_remove in names:
            updated_names = [name for name in names if name != name_to_remove]
            with open("giftsite/data/results.txt", "w") as file:
                file.write("\n".join(updated_names))
            return jsonify({"message": f"{name_to_remove} has been removed."})
        else:
            return jsonify({"message": f"{name_to_remove} was not found."})

    except FileNotFoundError:
        return jsonify({"error": "File not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
