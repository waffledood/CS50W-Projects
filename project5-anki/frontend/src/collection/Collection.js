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
          {cards.map((card) => {
            return (
              <>
                <Col key={`${card.id}q`}>
                  <div className={classes.card}>
                    <div className={classes.question}>{card.question}</div>
                  </div>
                </Col>
                <Col key={`${card.id}a`}>
                  <div className={classes.card}>
                    <div className={classes.answer}>{card.answer}</div>
                  </div>
                </Col>
              </>
            );
          })}
        </Row>
      </Container>
    </div>
  );
};

export default Collection;
