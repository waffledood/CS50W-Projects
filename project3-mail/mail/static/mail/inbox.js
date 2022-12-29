document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // When a user sends a mail
  document.querySelector('#compose-form').onsubmit = () => {
    // retrieve email contents from form
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
  
    // submit the POST request to send an email
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => {
      if (response.status >= 200 && response.status <= 299) {
        return response.json();
      } else {
        throw Error(response.statusText);
      }
    })
    .then(jsonResponse => {
      console.log(jsonResponse);
      // load user's sent mailbox
      load_mailbox('sent');
    }).catch(error => {
      // handle error
    });

    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Retrieve the relevant emails
  fetch(`/emails/${mailbox}`)
  .then(response => {
    if (response.status >= 200 && response.status <= 299) {
      return response.json();
    } else {
      throw Error(response.statusText);
    }
  })
  .then(emails => {
    // create div container for emails
    document.querySelector('#emails-view').innerHTML += '<div id="emails" class="list-group"></div>';

    // loop through json response of emails
    for (var key of Object.keys(emails)) {
      let emailJSONContent = emails[key];
      console.log(emailJSONContent);

      // create email HTML element
      let email = document.createElement('a');
      email.innerHTML = `
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1" id="email-subject">${emailJSONContent.subject}</h5>
          <small id="email-timestamp">${emailJSONContent.timestamp}</small>
        </div>
        <p class="mb-1" id="email-body">${emailJSONContent.body}</p>
        <small class="text-muted" id="email-recipients">${emailJSONContent.recipients.join(", ")}</small>
      `;

      // apply CSS styling to email
      email.className = `
        list-group-item list-group-item-action ${emailJSONContent.read == true ? 'text-muted' : ''}
        data-id="${emailJSONContent.id}"
      `;
      email.style = "cursor: pointer";

      // run load_mail function to email when it is clicked
      email.addEventListener('click', () => {
        load_mail(emailJSONContent.id);
      });

      // append email HTML element to emails class
      document.querySelector('#emails').append(email);
    }
  })
  .catch(error => {
    // handle error
    console.log(error);
  });

}

function load_mail(emailId) {
  // Show the individual mail and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  const emailView = document.querySelector('#email-view');

  // Retrieve the email
  fetch(`/emails/${emailId}`)
  .then(response => {
    if (response.status >= 200 && response.status <= 299) {
      return response.json();
    } else {
      throw Error(response.statusText);
    }
  })
  .then(emailJSONContent => {
    // set the class of emailView to a list group
    emailView.className = "list-group";

    // create the email list group item
    let email = document.createElement('a');
    email.innerHTML = `
      <div class="d-flex w-100 justify-content-between">
        <h5 class="mb-1" id="email-subject">${emailJSONContent.subject}</h5>
        <small id="email-timestamp">${emailJSONContent.timestamp}</small>
      </div>
      <p class="mb-1" id="email-body">${emailJSONContent.body}</p>
      <small class="text-muted" id="email-recipients">${emailJSONContent.recipients.join(", ")}</small>
    `;

    // apply CSS styling to email
    email.className = `
      list-group-item list-group-item-action ${emailJSONContent.read == true ? 'text-muted' : ''}
      data-id="${emailJSONContent.id}"
    `;
    email.style = "cursor: pointer";

    // insert email to email-view
    emailView.textContent = '';
    emailView.append(email);
  })
}
