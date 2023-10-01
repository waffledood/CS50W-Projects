import React from "react";
import { createRoot } from "react-dom/client";

import Collection from "./collection/Collection";

// Mount App to the mount point.
const rootElement = document.getElementById("app");
const collectionId = rootElement.getAttribute("data-collection-id");
const root = createRoot(rootElement);

console.log("index.js: collectionId,", collectionId);

const App = () => {
  return (
    <div>
      <Collection collectionId={collectionId} />
    </div>
  );
};

root.render(<App />);
