loadedFile = ""
canRun = true

document.getElementById('question').onkeydown = function(event) {
    if (event.keyCode == 13 && canRun) {
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

function askQuestion() {
    document.getElementById("buttonAsk").disabled = true;
    document.getElementById("buttonText").innerHTML = "Looking";
    document.getElementById("buttonSpinner").style.display = "block";
    document.getElementById("question").disabled = true;

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
        document.getElementById("answer").innerHTML = json[0]
        document.getElementById("answer").style.animation = ""
        document.getElementById("answer").style.animation = "fadeInAnimation ease 1s"
        document.getElementById("buttonAsk").disabled = false;
        document.getElementById("buttonText").innerHTML = "Ask";
        document.getElementById("buttonSpinner").style.display = "none";
        document.getElementById("question").disabled = false;
    })
}