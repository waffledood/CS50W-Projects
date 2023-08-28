import React from "react";

import classes from "./Collection.module.css";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

const Collection = () => {
  const cards = [
    {
      id: 1,
      question: "question 1",
      answer: "answer 1",
    },
    {
      id: 2,
      question: "question 2",
      answer: "answer 2",
    },
  ];

  return (
    <div>
      <h1>Collection</h1>
      <Container>
        <Row className="row-cols-2">
          <Col className={`${classes.header}`}>Question</Col>
          <Col className={`${classes.header}`}>Answer</Col>
        </Row>
        {cards.map((card) => {
          return (
            <Row className="row-cols-2" key={card.id}>
              <Col className={`${classes.card} ${classes.question}`}>
                {card.question}
              </Col>
              <Col className={`${classes.card} ${classes.answer}`}>
                {card.answer}
              </Col>
            </Row>
          );
        })}
      </Container>
    </div>
  );
};

export default Collection;
