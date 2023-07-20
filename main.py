from flask import Flask, jsonify, request, flash, redirect, Response, render_template
import os
import extract_text as et
import answer_question as aq
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/learn')
def learn():
    return render_template('learn.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.get('/getNotes')
def getNotes():
    notes = ["notes1.pdf", "notes2.pdf", "notes3.pdf"]
    return notes


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "GET":
        return render_template('upload.html')

    elif request.method == "POST":
        file_name = request.files['fileUpload'].filename

        # Check if no file was selected, TODO: create a popup for that (?)
        # Reloads the page if true
        if (file_name == ""):
            return render_template('upload.html')

        if 'gen' in request.form:
            if 'fileUpload' in request.files:
                # This is the actual pdf
                file = request.files['fileUpload']
                if file and file.filename != '':
                    file.save(os.path.join('./sentPDFs', file.filename))
            return render_template('learn.html')

        # Brings the user to the ask questions page
        elif 'ask' in request.form:
            return render_template('ask.html', file_name=file_name)


@app.get('/getFlashcards')
def login():
    args = request.args
    print(args)
    flashcards = []

    card = {}
    card["title"] = "mitosis"
    card["answer"] = "powerhouse of the cell"
    flashcards.append(card)

    card = {}
    card["title"] = "microcontroller"
    card["answer"] = "powerhouse of the computer"
    flashcards.append(card)

    card = {}
    card["title"] = "money"
    card["answer"] = "powerhouse of the bank"
    flashcards.append(card)
    return flashcards


@app.post('/ask')
def ask():
    if request.method == "POST":
        # Extract text from note into .txt and pickle file
        # If it already exists, no extraction is done
        # You can take this as the notes being stored into the cloud (maybe?)
        # TODO: A loading wheel while the note is being processed (may take around 30 seconds~ for long notes)
        et.extract_note(request.form.get("file_name"))

        note_name = request.form.get("file_name").split(".")[0]
        # Extract answer from note using question asked
        # Returns each answer as a list, not sure how to proceed from here (is JSON necessary?)
        # Maybe store in a text file in another directory, load as flash cards on the learn page?
        # use SQLite instead? ¯\_(ツ)_/¯
        answer_list = aq.answer(request.form.get("question"), note_name)

    return ("d")


if __name__ == '__main__':
    app.run(debug=True)
