import { useState } from "react";

import classes from "./ListYourHome.module.css";

const ListYourHome = (props) => {
  return (
    <div className={`${classes.div} default-font`}>
      <a className={`${classes.a} link`}>Airbnb your home</a>
    </div>
  );
};

export default ListYourHome;
