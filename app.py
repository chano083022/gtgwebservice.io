from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
import os
import logging

app = Flask(__name__)
CORS(app)

# Define the base directory and XML file path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
XML_FILE = os.path.join(BASE_DIR, "data.xml")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Function to load data from XML file
def load_data():
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
    except ET.ParseError as e:
        logging.error(f"Error parsing XML file: {e}")
        # Create a new root element if the file is empty
        root = ET.Element("root")
        tree = ET.ElementTree(root)
        tree.write(XML_FILE)
    return root

# Function to generate a unique ID for a new person
def generate_unique_id(existing_ids):
    if not existing_ids:
        return 1
    else:
        return max(existing_ids) + 1

# Function to extract person data from XML element
def extract_person_data(person):
    return {
        'id': person.findtext('id', default=''),
        'name': person.findtext('name', default=''),
        'age': person.findtext('age', default=''),
        'location': person.findtext('location', default=''),
        'phone': person.findtext('phone', default=''),
        'category': person.findtext('category', default=''),
        'location_event': person.findtext('location_event', default='')
    }

# Function to prettify XML for better readability
def prettify(elem, depth=0):
    if len(elem):
        elem.text = '\n' + '\t' * (depth + 1)
        for sub_elem in elem:
            prettify(sub_elem, depth + 1)
        sub_elem.tail = sub_elem.tail[:-1]
    elem.tail = '\n' + '\t' * depth

# Route to display the main page with all persons
@app.route('/')
def index():
    root = load_data()
    data = [extract_person_data(person) for person in root.findall('person')]
    return render_template('index.html', persons=data)

# Route to handle API request for all persons
@app.route('/api/data', methods=['GET'])
def get_data_api():
    root = load_data()
    data = [extract_person_data(person) for person in root.findall('person')]
    return jsonify(data)

# Route to add a new person
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    age = request.form['age']
    location = request.form['location']
    phone = request.form['phone']
    category = request.form['category']
    location_event = request.form['location_event']

    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    existing_ids = [int(person.findtext('id', default='')) for person in root.findall('person')]

    new_id = generate_unique_id(existing_ids)

    new_person = ET.Element('person')
    ET.SubElement(new_person, 'id').text = str(new_id)
    ET.SubElement(new_person, 'name').text = name
    ET.SubElement(new_person, 'age').text = age
    ET.SubElement(new_person, 'location').text = location
    ET.SubElement(new_person, 'phone').text = phone
    ET.SubElement(new_person, 'category').text = category
    ET.SubElement(new_person, 'location_event').text = location_event

    root.append(new_person)
    prettify(root)

    tree.write(XML_FILE)

    return redirect('/')

# Route to search for a person by ID
@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('search_id')
    root = load_data()

    data = []

    # Search for a specific user
    for person in root.findall('person'):
        if person.findtext('id', default='') == search_term:
            person_data = extract_person_data(person)
            data.append(person_data)

    return render_template('index.html', persons=data)

# Route to update a person by ID
@app.route('/update/<int:person_id>', methods=['PATCH', 'POST'])
def update(person_id):
    if request.method == 'PATCH':
        name = request.form['name']
        age = request.form['age']
        location = request.form['location']
        phone = request.form['phone']
        category = request.form['category']
        location_event = request.form['location_event']

        root = load_data()

        person_to_update = root.find(f"./person[id='{person_id}']")
        if person_to_update is not None:
            person_to_update.find('name').text = name
            person_to_update.find('age').text = age
            person_to_update.find('location').text = location
            person_to_update.find('phone').text = phone
            person_to_update.find('category').text = category
            person_to_update.find('location_event').text = location_event

            prettify(root)

            tree = ET.ElementTree(root)
            tree.write(XML_FILE)

        return redirect('/')
    else:
        return "Method Not Allowed", 405

# Route to delete a person by ID
@app.route('/delete/<int:person_id>', methods=['DELETE'])
def delete(person_id):
    root = load_data()

    person_to_delete = root.find(f"./person[id='{person_id}']")
    if person_to_delete is not None:
        root.remove(person_to_delete)

        prettify(root)

        tree = ET.ElementTree(root)
        tree.write(XML_FILE)

    return redirect('/')

# Route to refresh and display all persons
@app.route('/refresh', methods=['GET'])
def refresh():
    root = load_data()
    data = [extract_person_data(person) for person in root.findall('person')]
    return render_template('index.html', persons=data)

# Route to delete all persons
@app.route('/delete-all', methods=['DELETE'])
def delete_all():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    
    for person in root.findall('person'):
        root.remove(person)

    tree.write(XML_FILE)
    return redirect('/')

# Run the app
if __name__ == '__main__':
    # Explicitly set the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

