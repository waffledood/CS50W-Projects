import React, { useEffect, useState } from "react";

import classes from "./Collection.module.css";

import Container from "react-bootstrap/Container";
import ListGroup from "react-bootstrap/ListGroup";
import Table from "react-bootstrap/Table";

import { ThreeDots } from "react-bootstrap-icons";

const Collection = () => {
  const [collectionDetails, setCollectionDetails] = useState({});
  const [cards, setCards] = useState([]);
  const collectionId = 1;

  useEffect(() => {
    // fetch the cards in this collection
    fetch(`http://localhost:8000/anki/cards/${collectionId}`)
      .then((response) => {
        return response.json();
      })
      .then((cardsInCollection) => {
        setCards(cardsInCollection);
      });

    // fetch this collection's details
    fetch(`http://localhost:8000/anki/collection/${collectionId}`)
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
        <ListGroup className={classes.collectionDescription}>
          <ListGroup.Item>{collectionDetails["description"]}</ListGroup.Item>
        </ListGroup>
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
                    <ThreeDots />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </Table>
      </Container>
    </div>
  );
};

export default Collection;
