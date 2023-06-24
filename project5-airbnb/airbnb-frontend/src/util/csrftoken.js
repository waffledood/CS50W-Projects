import React from "react";
import { useState, useEffect } from "react";

import axios from "axios";

import config from "../config.json";

// The following function is copied from
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax

const CSRFToken = () => {
  const [CSRFToken, setCSRFToken] = useState("");

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        await axios.get(config.backendPort + config.api_getCSRFToken);
      } catch (err) {
        console.log(err);
      }
    };
    fetchData();
    setCSRFToken(getCookie("csrftoken"));
  }, []);

  return (
    <input
      type="hidden"
      id="csrfmiddlewaretoken"
      name="csrfmiddlewaretoken"
      value={CSRFToken}
    />
  );
};

export default CSRFToken;
