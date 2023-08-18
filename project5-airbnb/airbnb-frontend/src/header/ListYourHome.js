import { useState } from "react";

import classes from "./ListYourHome.module.css";
import ListYourHomeForm from "../form/ListYourHomeForm";

const ListYourHome = (props) => {
  const [listYourHomeClick, setListYourHomeClick] = useState(false);

  const listYourHomeActiveHandler = (props) => {
    setListYourHomeClick(true);
  };

  const listYourHomeInactiveHandler = (props) => {
    setListYourHomeClick(false);
  };

  return (
    <div className={`${classes.div} default-font`}>
      {listYourHomeClick && (
        <ListYourHomeForm onExit={listYourHomeInactiveHandler} />
      )}
      <a onClick={listYourHomeActiveHandler} className={`${classes.a} link`}>
        Airbnb your home
      </a>
    </div>
  );
};

export default ListYourHome;
