import React, { useEffect, useRef, useState, createRef } from "react";

import classes from "./Collection.module.css";

import CompleteCard from "../card/CompleteCard";
import EmptyCard from "../card/EmptyCard";

import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import ListGroup from "react-bootstrap/ListGroup";
import Table from "react-bootstrap/Table";
import Toast from "react-bootstrap/Toast";
import ToastContainer from "react-bootstrap/ToastContainer";

import { ThreeDots, Play, PlusLg } from "react-bootstrap-icons";

const Collection = (props) => {
  const [collectionDetails, setCollectionDetails] = useState({});
  const [cards, setCards] = useState([]);
  const collectionId = props.collectionId;

  const [showError, setShowError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const errorToast = (
    <ToastContainer className="p-3" position="bottom-end" style={{ zIndex: 1 }}>
      <Toast bg="danger">
        <Toast.Header>
          <strong className="me-auto">System Error</strong>
          <small>11 mins ago</small>
        </Toast.Header>
        <Toast.Body>{errorMessage}</Toast.Body>
      </Toast>
    </ToastContainer>
  );

  const [isAddingANewCard, setIsAddingANewCard] = useState(false);
  const emptyCardQuestionRef = useRef(null);
  const emptyCardAnswerRef = useRef(null);

  const createCardButtonHandler = () => {
    // retrieve new Card details
    const newCardQuestionValue = emptyCardQuestionRef.current.value;
    const newCardAnswerValue = emptyCardAnswerRef.current.value;

    // validate new Card details
    let cardIsValid = true;
    if (!newCardQuestionValue) {
      // new Card has an empty String for the Question field
      setErrorMessage("Question in new Card cannot be empty!");
      cardIsValid = false;
    } else if (newCardQuestionValue.length > 400) {
      // new Card has a Question longer than 400 characters
      setErrorMessage(
        "Question in new Card cannot be longer than 400 characters!"
      );
      cardIsValid = false;
    }
    if (!newCardAnswerValue) {
      // new Card has an empty String for the Answer field
      setErrorMessage((existingErrorMessage) => {
        if (existingErrorMessage) {
          return (existingErrorMessage +=
            "\nAnswer in new Card cannot be empty!");
        } else {
          return (existingErrorMessage +=
            "Answer in new Card cannot be empty!");
        }
      });
      cardIsValid = false;
    } else if (newCardAnswerValue.length > 400) {
      // new Card has an Answer longer than 400 characters
      setErrorMessage((existingErrorMessage) => {
        if (existingErrorMessage) {
          return (existingErrorMessage +=
            "\nAnswer in new Card cannot be longer than 400 characters!");
        } else {
          return (existingErrorMessage +=
            "Answer in new Card cannot be longer than 400 characters!");
        }
      });
      cardIsValid = false;
    }

    if (cardIsValid) {
      // create new Card
      const newCard = {
        user_id: window.userId,
        collection_id: collectionId,
        question: newCardQuestionValue,
        answer: newCardAnswerValue,
      };

      // submit POST request
      fetch("http://127.0.0.1:8000/anki/api/createCard", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newCard),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Unable to create Card!");
          }
          return response.json();
        })
        .then((json) => {
          // successful creation of Card
          const createdCard = json.card;
          const successMessage = json.message;

          console.log("createdCard:", createdCard);

          // set isAddingANewCard to false, as new Card has been created
          setIsAddingANewCard(false);

          // add created Card to cards component
          setCards((prevCards) => {
            return [...prevCards, createdCard];
          });
        })
        .catch((error) => {
          // error handling for UI using error boundary
          console.log("error: ", error.message);
          setShowError(true);
          setErrorMessage(error.message);
        });
    } else {
      setShowError(true);
    }
  };

  const addCardButtonHandler = () => {
    // toggle the state of isAddingANewCard
    setIsAddingANewCard((prev) => {
      return !prev;
    });
    console.log("Add card button clicked");
  };

  const activeRecallURL = `http://127.0.0.1:8000/anki/activeRecall/${collectionId}`;

  const emptyCard = (
    <EmptyCard
      listId={cards.length + 1}
      questionRef={emptyCardQuestionRef}
      answerRef={emptyCardAnswerRef}
      createCardHandler={createCardButtonHandler}
    />
  );

  useEffect(() => {
    // fetch the cards in this collection
    fetch(`http://127.0.0.1:8000/anki/api/cards/${collectionId}`)
      .then((response) => {
        return response.json();
      })
      .then((cardsInCollection) => {
        setCards(cardsInCollection);
      });

    // fetch this collection's details
    fetch(`http://127.0.0.1:8000/anki/api/collection/${collectionId}`)
      .then((response) => {
        return response.json();
      })
      .then((collection) => {
        setCollectionDetails({
          name: collection["name"],
          description: collection["description"],
          date_created: collection["date_created"],
          date_modified: collection["date_modified"],
        });
      });
  }, []);

  return (
    <div className={classes.collection}>
      <Container>
        <h1>{collectionDetails["name"]}</h1>
        <div className="d-flex flex-row justify-content-between align-items-center">
          <div>
            <ListGroup className={classes.collectionDescription}>
              <ListGroup.Item>
                {collectionDetails["description"]}
              </ListGroup.Item>
            </ListGroup>
          </div>
          <div className="d-inline-flex align-items-center">
            <button
              type="button"
              className="btn btn-primary"
              onClick={addCardButtonHandler}
            >
              Add Card
            </button>
            <a
              type="button"
              className="btn btn-success ms-3 px-0 py-0"
              href={activeRecallURL}
            >
              <Play size={36} />
            </a>
          </div>
        </div>
      </Container>
      <Container>
        <hr />
        <Table hover={true}>
          <thead>
            <tr>
              <th>#</th>
              <th>Question</th>
              <th>Answer</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {cards.map((card, i) => {
              return <CompleteCard key={card.id} card={card} listId={i + 1} />;
            })}
            {isAddingANewCard && emptyCard}
          </tbody>
        </Table>
      </Container>

      {
        <ToastContainer
          className="p-3"
          position="bottom-end"
          style={{ zIndex: 1 }}
        >
          <Toast
            bg="danger"
            onClose={() => setShowError(false)}
            show={showError}
            delay={3000}
            autohide
          >
            <Toast.Header>
              <strong className="me-auto">System Error</strong>
              <small>Just now</small>
            </Toast.Header>
            <Toast.Body>{errorMessage}</Toast.Body>
          </Toast>
        </ToastContainer>
      }
    </div>
  );
};

export default Collection;
