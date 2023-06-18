import React from "react";

import classes from "./ListYourHomeForm.module.css";

const ListYourHomeForm = (props) => {
  const formSubmitHandler = (event) => {
    // stop form submission
    event.preventDefault();

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

export default ListYourHomeForm;
