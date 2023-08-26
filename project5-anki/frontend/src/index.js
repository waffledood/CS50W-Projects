import React from "react";
import ReactDOM from "react-dom";

const App = () => {
  return <div>Hello!</div>;
};

// Mount App to the mount point.
const root = document.getElementById("app");
ReactDOM.render(<App />, root);
