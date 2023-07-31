loadedFile = ""
answers = []
answerIndex = 0

document.getElementById('question').onkeydown = function(event) {
    if (event.keyCode == 13) {
        askQuestion()
    }
}

fetch("/getNotes")
.then(notes => notes.json())
.then(json => {
    notesList = document.getElementById("learnPdfList")
    flashcardIndex = 0
    for (let i =0;i < json.length;i++) {
        console.log(json[i])
        var node = document.createElement("li")
        node.classList.add("nav-item")

        var innerLink = document.createElement("a")
        innerLink.classList.add("nav-link")
        if (i == 0) { innerLink.classList.add("active") }
        innerLink.setAttribute("id", `notesIndex${i}`)
        innerLink.setAttribute("data-toggle", "tab")
        innerLink.setAttribute("style", "color: white;")
        innerLink.innerHTML = json[i]
        innerLink.addEventListener("click", function() {tabsChanged(json[i])})
        node.appendChild(innerLink)
        notesList.appendChild(node)
    }
    tabsChanged(json[0])
})

function tabsChanged(name) {
    loadedFile = name
    document.getElementById("NotesHeader").innerHTML = `Current file loaded: ${name}`
}

function decAnswer() {
    answerIndex-= 1
    if (answerIndex == 0)
    {
        document.getElementById("goUpButton").style.display = "none"
    }
    else
    {
        document.getElementById("goUpButton").style.display = "block"
    }
    document.getElementById("goDownButton").style.display = "block"

    updateAnswer()
}

function incAnswer() {
    answerIndex += 1
    if (answerIndex == answers.length-1) {
        document.getElementById("goDownButton").style.display = "none"
    }
    else
    {
        document.getElementById("goDownButton").style.display = "block"
    }
    document.getElementById("goUpButton").style.display = "block"


    updateAnswer()
}

function updateAnswer() {
    var element = document.getElementById("answer")
    element.innerHTML = answers[answerIndex]
    element.style.animation = "none"
    element.offsetHeight
    element.style.animation = "fadeInAnimation ease 1s"
}

function askQuestion() {
    document.getElementById("buttonAsk").disabled = true;
    document.getElementById("buttonText").innerHTML = "Looking";
    document.getElementById("buttonSpinner").style.display = "block";
    document.getElementById("question").disabled = true;

    answers = []
    answerIndex = 0
    var questionAsked = document.getElementById("question").value
    if (questionAsked.length == 0) { return; }
    fetch("/ask", {
        method : "POST",
        headers: {
            "Content-Type": "application/json",
          },      
        body : JSON.stringify({
            file : loadedFile,
            question : questionAsked
        })
    })
    .then(res => res.json())
    .then(json => {
        console.log(json)
        answers = json
        answerIndex = 0
        updateAnswer()
        document.getElementById("buttonAsk").disabled = false;
        document.getElementById("buttonText").innerHTML = "Ask";
        document.getElementById("buttonSpinner").style.display = "none";
        document.getElementById("question").disabled = false;
        document.getElementById("goDownButton").style.display = "block"
    })
}