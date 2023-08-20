import React from "react";
import ReactDOM from "react-dom";

import Login from "./login/Login";

const App = () => {
  return <Login />;
};

// Mount App to the mount point.
const root = document.getElementById("app");
ReactDOM.render(<App />, root);
