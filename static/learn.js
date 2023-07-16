flashcards = []

// $(document).ready(function(){
//     $("#flashcardModal").modal('show');
// });

var flippedBack = false
var flashcardIndex = 0

$("#popupCard").click(function() {
    if (flippedBack) {
        document.getElementById("popupInner").classList.remove("flipCard")
    }
    else {
        document.getElementById("popupInner").classList.add("flipCard")
    }
    flippedBack = !flippedBack
})

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
    fetch(`/getFlashcards?cards=${name}`)
    .then(res => res.json())
    .then(json => {
        cardsList = document.getElementById("cardsList")
        cardsList.innerHTML = ""
        flashcards = json
        for (let i = 0;i < flashcards.length;i++) {
            var column = document.createElement("div")
            column.classList.add("col")
            column.classList.add("pb-3")

            var card = document.createElement("div")
            card.classList.add("card")

            $(card).click(function() {
                document.getElementById("popupFront").innerHTML = flashcards[i]["title"]
                document.getElementById("popupBack").innerHTML = flashcards[i]["answer"]
                $("#flashcardModal").modal('show');
            })
            
            var body = document.createElement("div")
            body.classList.add("card-body")
            body.classList.add("rounded-3")
            body.innerHTML = flashcards[i]["title"]

            card.appendChild(body)
            column.appendChild(card)

            cardsList.appendChild(column)
        }
    })
}