var listOfCards = [];

function initializeListOfCards() {
  // retrieve all Cards for this Collection
  // TODO: Retrieve Cards from DB
  listOfCards = [
    {
      id: 1,
      collection_id: 1,
      question: "question for 1",
      answer: "answer for 1",
    },
    {
      id: 2,
      collection_id: 1,
      question: "question for 2",
      answer: "answer for 2",
    },
    {
      id: 4,
      collection_id: 1,
      question: "question for 4",
      answer: "answer for 4",
    },
    {
      id: 7,
      collection_id: 1,
      question: "question for 7",
      answer: "answer for 7",
    },
  ];
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
