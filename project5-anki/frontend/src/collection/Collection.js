import React, { useEffect, useState, createRef } from "react";

import classes from "./Collection.module.css";

import Card from "../card/Card";

import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import ListGroup from "react-bootstrap/ListGroup";
import Table from "react-bootstrap/Table";
import Toast from "react-bootstrap/Toast";
import ToastContainer from "react-bootstrap/ToastContainer";

import { ThreeDots, Play, PlusLg } from "react-bootstrap-icons";

const Collection = () => {
  const [collectionDetails, setCollectionDetails] = useState({});
  const [cards, setCards] = useState([]);
  const collectionId = 1;

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
  const newCardQuestionRef = createRef();
  const newCardAnswerRef = createRef();

  const [hasAddedANewCard, setHasAddedANewCard] = useState(false);
  const [newCompleteCard, setNewCompleteCard] = useState();

  const createCardButtonHandler = () => {
    // retrieve new Card details
    const newCardQuestionValue = newCardQuestionRef.current.value;
    const newCardAnswerValue = newCardAnswerRef.current.value;

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
        collection_id: collectionId,
        question: newCardQuestionValue,
        answer: newCardAnswerValue,
      };

      // submit POST request
      fetch("http://127.0.0.1:8000/anki/createCard", {
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

          // set hasAddedANewCard to true, as new Card has been created
          setHasAddedANewCard(true);
          // set isAddingANewCard to false, as new Card has been created
          setIsAddingANewCard(false);

          // create new complete Card component
          setNewCompleteCard(
            <Card
              id={createdCard.id}
              cards={cards}
              question={createdCard.question}
              answer={createdCard.answer}
            />
          );
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

  const emptyCard = (
    <tr>
      <td>{cards.length + 1}</td>
      <td>
        <textarea
          name=""
          id=""
          cols="1"
          rows="1"
          placeholder="New Question..."
          ref={newCardQuestionRef}
        ></textarea>
      </td>
      <td>
        <textarea
          name=""
          id=""
          cols="1"
          rows="1"
          placeholder="New Answer..."
          ref={newCardAnswerRef}
        ></textarea>
      </td>
      <td>
        <Button
          variant="success"
          className="px-1 py-1 d-inline-flex justify-content-center align-items-center"
          onClick={createCardButtonHandler}
        >
          <PlusLg />
        </Button>
      </td>
    </tr>
  );

  useEffect(() => {
    // fetch the cards in this collection
    fetch(`http://127.0.0.1:8000/anki/cards/${collectionId}`)
      .then((response) => {
        return response.json();
      })
      .then((cardsInCollection) => {
        setCards(cardsInCollection);
      });

    // fetch this collection's details
    fetch(`http://127.0.0.1:8000/anki/collection/${collectionId}`)
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
            <button type="button" className="btn btn-success ms-3 px-0 py-0">
              <Play size={36} />
            </button>
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
              return (
                <tr key={card.id}>
                  <td>{i + 1}</td>
                  <td>{card.question}</td>
                  <td>{card.answer}</td>
                  <td>
                    <Button
                      variant="secondary"
                      className="px-1 py-1 d-inline-flex justify-content-center align-items-center"
                    >
                      <ThreeDots />
                    </Button>
                  </td>
                </tr>
              );
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
