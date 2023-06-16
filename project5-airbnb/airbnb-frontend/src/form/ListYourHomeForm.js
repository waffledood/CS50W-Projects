import React from "react";
import ReactDOM from "react-dom";

import classes from "./ListYourHomeForm.module.css";

const Backdrop = (props) => {
  return <div className={classes.backdrop} onClick={props.onExit}></div>;
};

const ModalOverlay = (props) => {
  const formSubmitHandler = (event) => {
    // stop form submission
    event.preventDefault();

    // close the modal overlay
    props.onExit();

    // handle form submission
  };

  return (
    <div className={classes.modal}>
      <form action="#" onSubmit={formSubmitHandler}>
        <div className={classes.formControl}>
          <label htmlFor="listingName">Name</label>
          <input type="text" name="listingName" id="listingName" />
        </div>

        <div className={classes.formControl}>
          <label htmlFor="listingDescription">Description</label>
          <textarea
            name="listingDescription"
            id="listingDescription"
          ></textarea>
        </div>

        <div className={classes.formControl}>
          <label htmlFor="listingPriceNightly">Price (Nightly)</label>
          <input
            type="number"
            name="listingPriceNightly"
            id="listingPriceNightly"
          />
        </div>

        <br />

        <div className={classes.formControl}>
          <button type="submit" className="btn">
            Submit
          </button>
        </div>
      </form>
    </div>
  );
};

const ListYourHomeForm = (props) => {
  return (
    <React.Fragment>
      {ReactDOM.createPortal(
        <Backdrop onExit={props.onExit} />,
        document.getElementById("backdrop-root")
      )}
      {ReactDOM.createPortal(
        <ModalOverlay onExit={props.onExit} />,
        document.getElementById("overlay-root")
      )}
    </React.Fragment>
  );
};

export default ListYourHomeForm;
