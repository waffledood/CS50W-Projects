import React from "react";

import Button from "react-bootstrap/Button";

import { ThreeDots } from "react-bootstrap-icons";

const Card = (props) => {
  return (
    <tr key={props.id}>
      <td>{props.cards.length + 1}</td>
      <td>{props.question}</td>
      <td>{props.answer}</td>
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
};

export default Card;
