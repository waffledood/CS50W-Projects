import React from "react";

import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const Login = (props) => {
  return (
    <div className="mx-auto p-3">
      <Form>
        <Form.Group className="mb-3" controlId="loginFormUsername">
          <Form.Label>Username</Form.Label>
          <Form.Control type="email" placeholder="Enter username" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="loginFormPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Enter your password" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="loginFormCheckbox">
          <Form.Check type="checkbox" label="Keep me signed in" />
        </Form.Group>

        <Button variant="primary" type="submit">
          Log In
        </Button>
      </Form>
      Don't have an account? <a href="#">Register</a>
    </div>
  );
};

export default Login;
