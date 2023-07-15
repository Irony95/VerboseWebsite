from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/upload')
def upload():
   return render_template('upload.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.get('/getFlashcards')
def login():
   flashcards = {}
   flashcards["mitosis"] = "powerhouse of the cell"
   return flashcards

if __name__ == '__main__':
   app.run(debug=True)