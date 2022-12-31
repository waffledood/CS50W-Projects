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
        <small class="text-muted" id="email-sender">${emailJSONContent.sender}</small>
      `;

      // apply CSS styling to email
      email.className = `
        list-group-item list-group-item-action ${emailJSONContent.read == true ? 'text-muted' : ''}
        data-id="${emailJSONContent.id}"
      `;
      email.style = "cursor: pointer";

      // run these functions when an email is clicked
      email.addEventListener('click', () => {
        // load the specified mail
        load_mail(emailJSONContent.id);

        // mark the email as read
        fetch(`/emails/${emailJSONContent.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        });
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
    // create utilities div (to store utilities-related buttons & functions)
    const utilitiesDiv = document.createElement('div');
    utilitiesDiv.className = `d-flex w-100`;

    // create archive button
    const archiveBtn = document.createElement('button');
    archiveBtn.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive" viewBox="0 0 16 16">
        <path d="M0 2a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1v7.5a2.5 2.5 0 0 1-2.5 2.5h-9A2.5 2.5 0 0 1 1 12.5V5a1 1 0 0 1-1-1V2zm2 3v7.5A1.5 1.5 0 0 0 3.5 14h9a1.5 1.5 0 0 0 1.5-1.5V5H2zm13-3H1v2h14V2zM5 7.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z"/>
      </svg>
    `;
    archiveBtn.type = 'button';
    archiveBtn.className = 'btn btn-outline-secondary mt-2';
    archiveBtn.addEventListener('click', () => {
      console.log('archived');
      // mark the email as archived
      fetch(`/emails/${emailJSONContent.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      });
    });

    // add tooltip to archive button
    archiveBtn.setAttribute('data-bs-toggle', 'tooltip');
    archiveBtn.setAttribute('data-bs-title', 'Archive');

    // add archive button to utilities div
    utilitiesDiv.append(archiveBtn);

    // create the email list group item
    let email = document.createElement('div');

    // add utilites div to the top of the email element
    email.append(utilitiesDiv);

    // define the rest of the email element
    let emailContent = document.createElement('div');
    emailContent.innerHTML = `
      <hr>
      <div class="d-flex w-100 justify-content-between">
        <h5 class="mb-1" id="email-subject">${emailJSONContent.subject}</h5>
        <small id="email-timestamp">${emailJSONContent.timestamp}</small>
      </div>
      <small class="text-muted" id="email-sender">From: ${emailJSONContent.sender}</small>
      <br>
      <small class="text-muted" id="email-recipients">To: ${emailJSONContent.recipients.join(", ")}</small>
      <hr>
      <p class="mb-1" id="email-body">${emailJSONContent.body}</p>
    `;

    email.append(emailContent);

    // apply CSS styling to email
    email.className = `
      list-group-item ${emailJSONContent.read == true ? 'text-muted' : ''}
      data-id="${emailJSONContent.id}"
    `;

    // set the class of emailView to a list group
    emailView.className = "list-group";

    // insert email to email-view
    emailView.textContent = '';
    emailView.append(email);

    // load Tooltips
    loadToolTips();
  })
  .catch(error => {
    // handle error
    console.log(error);
  })
}

function loadToolTips() {
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}
