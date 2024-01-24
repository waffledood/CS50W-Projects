var listOfCards = [];

function initializeListOfCards() {
  // retrieve all Cards for this Collection
  listOfCards = JSON.parse(
    document.getElementById("list-of-cards").textContent
  );
}

function revealCardAnswer() {
  const cardAnswerDiv = document.querySelector("#cardAnswer");
  const cardAnswerClasses = cardAnswerDiv.className.split(" ");

  const cardAnswerUpdatedClasses = cardAnswerClasses.map((elem) => {
    if (elem !== "d-none") {
      return elem;
    } else {
      return "d-block";
    }
  });

  cardAnswerDiv.className = cardAnswerUpdatedClasses.join(" ");
}

function initializeNewCard() {
  const randomInt = Math.floor(Math.random() * listOfCards.length);
  const randomCard = listOfCards[randomInt];

  document.querySelector("#cardId").dataset.cardId = randomCard.id;
  document.querySelector("#cardQuestion").innerHTML = randomCard.question;
  document.querySelector("#cardAnswer").innerHTML = randomCard.answer;
}

function nextCardClick() {
  const currentCardId = document.querySelector("#cardId").dataset.cardId;

  // remove current Card from list of Cards
  listOfCards = listOfCards.filter((card) => card.id != currentCardId);

  // when all Cards have been recalled, display the success page
  if (listOfCards.length == 0) {
    // TODO: Display success page
    return;
  }

  initializeNewCard();
}

document.addEventListener("DOMContentLoaded", function () {
  initializeListOfCards();
  initializeNewCard();

  // add functionality to Active Recall
  const nextCard = document.querySelector("#nextCard");
  nextCard?.addEventListener("click", nextCardClick, false);
});
