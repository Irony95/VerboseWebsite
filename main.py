from flask import Flask, jsonify, request, flash, redirect, Response, render_template
import os
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
        if 'fileUpload' in request.files:
            # This is the actual pdf
            file = request.files['fileUpload']
            if file and file.filename != '':
                file.save(os.path.join('./sentPDFs', file.filename))

        return render_template('learn.html')

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

if __name__ == '__main__':
   app.run(debug=True)