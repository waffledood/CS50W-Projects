import React from "react";

const Card = (props) => {
  return (
    <tr key={props.id}>
      <td>{props.cards.length + 1}</td>
      <td>{props.question}</td>
      <td>{props.answer}</td>
      <td>{props.button}</td>
    </tr>
  );
};

export default Card;
