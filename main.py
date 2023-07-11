from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/style.css')
def css():
   return render_template('style.css')

@app.get('/getFlashcards')
def login():
   flashcards = {}
   flashcards["mitosis"] = "powerhouse of the cell"
   return flashcards

if __name__ == '__main__':
   app.run()