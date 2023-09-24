import React from "react";

import Card from "./Card";

import Button from "react-bootstrap/Button";

import { ThreeDots } from "react-bootstrap-icons";

const CompleteCard = (props) => {
  const detailsButton = (
    <Button
      variant="secondary"
      className="px-1 py-1 d-inline-flex justify-content-center align-items-center"
    >
      <ThreeDots />
    </Button>
  );

  return (
    <Card
      id={props.id}
      cards={props.cards}
      question={props.question}
      answer={props.answer}
      button={detailsButton}
    />
  );
};

export default CompleteCard;
