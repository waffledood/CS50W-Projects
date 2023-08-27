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
          {"Placeholder value for testing purposes."}
        </Row>
      </Container>
    </div>
  );
};

export default Collection;
