import React from "react";

const Card = (props) => {
  return (
    <tr>
      <td>{props.listId}</td>
      <td>{props.question}</td>
      <td>{props.answer}</td>
      <td>{props.button}</td>
    </tr>
  );
};

export default Card;
