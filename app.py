from flask import Flask, render_template, request, jsonify
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)
XML_FILE = 'user_data.xml'

# Initialize XML if not exists
if not os.path.exists(XML_FILE):
    root = ET.Element("users")
    tree = ET.ElementTree(root)
    tree.write(XML_FILE)

def read_users():
    tree = ET.parse(XML_FILE)
    return tree.getroot()

def save_user(data):
    root = read_users()
    user = ET.SubElement(root, "user")
    for key, value in data.items():
        ET.SubElement(user, key).text = value
    ET.ElementTree(root).write(XML_FILE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    save_user(data)
    return jsonify({"message": "Registration successful!"})

@app.route('/login', methods=['POST'])
def login():
    req = request.json
    root = read_users()
    for user in root.findall("user"):
        if (user.find("uid").text == req["uid"] and 
            user.find("serviceNow").text == req["serviceNow"]):
            return jsonify({"message": f"Login successful. Welcome {user.find('accountName').text}!"})
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
