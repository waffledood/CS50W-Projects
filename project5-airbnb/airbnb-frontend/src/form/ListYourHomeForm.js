import React from "react";
import ReactDOM from "react-dom";

import classes from "./ListYourHomeForm.module.css";

const Backdrop = (props) => {
  return <div className={classes.backdrop} onClick={props.onExit}></div>;
};
const ListYourHomeForm = (props) => {
  return (
    <React.Fragment>
      {ReactDOM.createPortal(
        <Backdrop onExit={props.onExit} />,
        document.getElementById("backdrop-root")
      )}
    </React.Fragment>
  );
};

export default ListYourHomeForm;
