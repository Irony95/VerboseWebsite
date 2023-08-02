var flippedBack = false
var flashcardIndex = 0
var flashcards = [];

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
    if (name.trim().length > 0) {
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
                    flashcardIndex = i
                    updatePopupCard()
                    $("#flashcardModal").modal('show');
                })
                
                var body = document.createElement("div")
                body.classList.add("card-body")
                body.classList.add("rounded-3")
                body.innerHTML = flashcards[i]["keyword"]

                card.appendChild(body)
                column.appendChild(card)

                cardsList.appendChild(column)
            }
        })
    } else {
        fetch("/getFlashcards")
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
                    flashcardIndex = i
                    updatePopupCard()
                    $("#flashcardModal").modal('show');
                })
                
                var body = document.createElement("div")
                body.classList.add("card-body")
                body.classList.add("rounded-3")
                body.innerHTML = flashcards[i]["keyword"]

                card.appendChild(body)
                column.appendChild(card)

                cardsList.appendChild(column)
            }
        })
    }
}

function dismissPopup() {
    console.log("asdfasdf")
    $("#flashcardModal").modal('hide');
}

function goLeft() {
    if (flashcardIndex == 0) { return }
    flashcardIndex--
    updatePopupCard()
}

function goRight() {
    if (flashcardIndex == flashcards.length-1) { return }
    flashcardIndex++
    updatePopupCard()
}

function updatePopupCard() {
    // console.log(flashcardIndex)
    document.getElementById("popupFront").innerHTML = flashcards[flashcardIndex]["keyword"]
    document.getElementById("popupBack").innerHTML = flashcards[flashcardIndex]["definition"]

    var popup = document.getElementById("popupCard")
    popup.style.animation = "none"
    popup.offsetHeight
    popup.style.animation = "fadeInAnimation ease 1s, MoveUpDown ease 1s"
}

function updateFlashcardData() {
    var newKeyword = document.getElementById("newKeyword").value;
    var newDefinition = document.getElementById("newDefinition").value;
    flashcards[flashcardIndex]["keyword"] = newKeyword;
    flashcards[flashcardIndex]["definition"] = newDefinition;
    var formData = new FormData();
    formData.append('flashcardIndex', flashcardIndex);
    formData.append('newKeyword', newKeyword);
    formData.append('newDefinition', newDefinition);

    fetch('/updateFlashcard', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            flashcards[flashcardIndex]["keyword"] = newKeyword;
            flashcards[flashcardIndex]["definition"] = newDefinition;
            tabsChanged(''); 
        }
    });
}

document.getElementById("newKeyword").addEventListener("input", updateFlashcardData);
document.getElementById("newDefinition").addEventListener("input", updateFlashcardData);

function showUpdateForm() {
    var updateForm = document.getElementById("updateForm");
    if (updateForm.style.display === "none") {
        updateForm.style.display = "block";
    } else {
        updateForm.style.display = "none";
    }
    updatePopupCard();
    updateFlashcardData();
}



