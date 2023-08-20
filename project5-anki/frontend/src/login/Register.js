import React from "react";

import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const Register = (props) => {
  return (
    <Form>
      <Form.Group className="mb-3" controlId="registerFormUsername">
        <Form.Label>Username</Form.Label>
        <Form.Control type="email" placeholder="Enter username" />
      </Form.Group>

      <Form.Group className="mb-3" controlId="registerFormPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Enter your password" />
        <Form.Text id="passwordHelpBlock" muted>
          Your password must be 6-15 characters long, contain letters and
          numbers, and must not contain spaces, special characters, or emoji.
        </Form.Text>
      </Form.Group>

      <Form.Group className="mb-3" controlId="confirmation">
        <Form.Label>Confirm Your Password</Form.Label>
        <Form.Control type="password" placeholder="Confirm your password" />
      </Form.Group>

      <Button variant="primary" type="submit">
        Create Account
      </Button>
    </Form>
  );
};

export default Register;
