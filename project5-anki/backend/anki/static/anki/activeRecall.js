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

function hideCardAnswer() {
  const cardAnswerDiv = document.querySelector("#cardAnswer");
  const cardAnswerClasses = cardAnswerDiv.className.split(" ");

  const cardAnswerUpdatedClasses = cardAnswerClasses.map((elem) => {
    if (elem !== "d-block") {
      return elem;
    } else {
      return "d-none";
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

function showAnswerClick() {
  // disable "Show Answer" button after it is clicked
  const showAnswerButton = document.querySelector("#showAnswer");
  showAnswerButton.disabled = true;

  revealCardAnswer();

  const currentCardId = document.querySelector("#cardId").dataset.cardId;

  // remove current Card from list of Cards
  listOfCards = listOfCards.filter((card) => card.id != currentCardId);

  // enable "Next Card" button after "Show Answer" is clicked
  const nextCardButton = document.querySelector("#nextCard");
  if (listOfCards.length != 0) {
    nextCardButton.disabled = false;
  } else {
    nextCardButton.disabled = true;
  }
}

function nextCardClick() {
  // when all Cards have been recalled, display the success page
  if (listOfCards.length == 0) {
    // TODO: Display success page
    return;
  }

  hideCardAnswer();

  initializeNewCard();

  // re-enable "Show Answer" button if it has been clicked
  document.querySelector("#showAnswer").disabled = false;

  // disable "Next Card" button
  document.querySelector("#nextCard").disabled = true;
}

document.addEventListener("DOMContentLoaded", function () {
  initializeListOfCards();
  initializeNewCard();

  // add functionality to Active Recall
  const nextCard = document.querySelector("#nextCard");
  nextCard?.addEventListener("click", nextCardClick, false);

  // add functionality to "Show Answer" button
  const showAnswer = document.querySelector("#showAnswer");
  showAnswer?.addEventListener("click", showAnswerClick, false);
});
