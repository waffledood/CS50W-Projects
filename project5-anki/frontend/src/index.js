import React from "react";
import { createRoot } from "react-dom/client";

import Collection from "./collection/Collection";

const App = () => {
  return (
    <div>
      <Collection />
    </div>
  );
};

// Mount App to the mount point.
const rootElement = document.getElementById("app");
const root = createRoot(rootElement);

root.render(<App />);
