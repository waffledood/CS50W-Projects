import React from "react";
import ReactDOM from "react-dom";

import Collection from "./collection/Collection";

const App = () => {
  return (
    <>
      <Collection />
    </>
  );
};

// Mount App to the mount point.
const root = document.getElementById("app");
ReactDOM.render(<App />, root);
