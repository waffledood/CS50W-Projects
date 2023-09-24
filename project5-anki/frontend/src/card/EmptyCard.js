import React from "react";

import Card from "./Card";

import Button from "react-bootstrap/Button";

import { PlusLg } from "react-bootstrap-icons";

const EmptyCard = (props) => {
  const addButton = (
    <Button
      variant="success"
      className="px-1 py-1 d-inline-flex justify-content-center align-items-center"
      onClick={props.createCardHandler}
    >
      <PlusLg />
    </Button>
  );

  const emptyCardQuestion = (
    <textarea
      name=""
      id=""
      cols="1"
      rows="1"
      placeholder="New Question..."
      ref={props.questionRef}
    ></textarea>
  );

  const emptyCardAnswer = (
    <textarea
      name=""
      id=""
      cols="1"
      rows="1"
      placeholder="New Answer..."
      ref={props.answerRef}
    ></textarea>
  );

  return (
    <Card
      listId={props.listId}
      question={emptyCardQuestion}
      answer={emptyCardAnswer}
      button={addButton}
    />
  );
};

export default EmptyCard;
