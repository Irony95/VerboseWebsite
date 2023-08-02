from flask import Flask, jsonify, request, flash, redirect, Response, render_template, session
import os
import extract_text as et
import answer_question as aq
import generate_flashcards as gf
import json
app = Flask(__name__)

FLASH_CARDS = "flashcards.json"

app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/learn')
def learn():
    return render_template('flashcards.html')

@app.route('/QnANotes')
def QnANotes():
    return render_template('ask.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.get('/getNotes')
def getNotes():
    notes = os.listdir('./sentPDFs')
    return notes

#### Upload the file
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "GET":
        return render_template('upload.html')

    elif request.method == "POST":
        file_name = request.files['fileUpload'].filename

        if (file_name == ""):
            return render_template('upload.html')

        if 'fileUpload' in request.files:
            file = request.files['fileUpload']
            if file and file.filename != '':
                file.save(os.path.join('./sentPDFs', file.filename))
                print("extracting...")
                et.extract_note(file.filename)
                print("extracted")
        return render_template('upload.html')
    
#### Generate Flashcards

@app.get('/getFlashcards')
def login():
    args = request.args
    cards_value = args.get('cards')
    flashcards = []

    if cards_value and len(cards_value.strip()) > 0:
        cards_value2 = cards_value.split(".")[0]
        generated_flashcards = gf.get_keywords_with_definitions(cards_value2)

        for gf.keyword, _, gf.definition in generated_flashcards:
            card = {}
            card["keyword"] = gf.keyword
            card["definition"] = gf.definition
            flashcards.append(card)

        write_flashcards(flashcards)
        session['flashcards'] = flashcards
    else:
        flashcards = read_flashcards()

    return jsonify(flashcards)

#### Generate Questions

@app.post('/ask')
def ask():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        print(json)
        # Extract text from note into .txt and pickle file
        # If it already exists, no extraction is done
        # You can take this as the notes being stored into the cloud (maybe?)
        # TODO: A loading wheel while the note is being processed (may take around 30 seconds~ for long notes)


        note_name = json["file"].split(".")[0]
        # Extract answer from note using question asked
        # Returns each answer as a list, not sure how to proceed from here (is JSON necessary?)
        # Maybe store in a text file in another directory, load as flash cards on the learn page?
        # use SQLite instead? ¯\_(ツ)_/¯
        answer_list = aq.answer(json["question"], note_name)

        return answer_list


####Update the flashcard and write it to json

@app.post('/updateFlashcard')
def update_flashcard():
    flashcard_index = int(request.form.get('flashcardIndex'))
    new_keyword = request.form.get('newKeyword')
    new_definition = request.form.get('newDefinition')

    flashcards = session.get('flashcards', [])
    flashcards[flashcard_index]["keyword"] = new_keyword
    flashcards[flashcard_index]["definition"] = new_definition

    session['flashcards'] = flashcards
    write_flashcards(flashcards)

    return jsonify(success=True)


#### Saving file into a json
def read_flashcards():
    try:
        with open(FLASH_CARDS, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_flashcards(flashcards):
    with open(FLASH_CARDS, "w") as file:
        json.dump(flashcards, file)

if __name__ == '__main__':
    app.run(debug=True)

