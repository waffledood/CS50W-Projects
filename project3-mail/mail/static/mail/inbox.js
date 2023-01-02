document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => {
    compose_email();
  });

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(cpRcpt = '', cpSbj = '', cpBody = '') {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = cpRcpt;
  document.querySelector('#compose-subject').value = cpSbj;
  document.querySelector('#compose-body').value = cpBody;

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
        <div class="d-flex w-100 justify-content-between">
          <small class="text-muted" id="email-sender">${emailJSONContent.sender}</small>
          <div class="position-relative">
            <div class="position-absolute top-50 end-0 translate-middle-y ${emailJSONContent.read == true ? 'visually-hidden' : ''}">
              <span class="badge bg-primary rounded-circle p-2">
                <span class="visually-hidden">New alerts</span>
              </span>
            </div>
          </div>
        </div>
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
        load_mail(emailJSONContent.id, mailbox);

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

function load_mail(emailId, mailbox) {
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

    // create archive button only when the mailbox is 'inbox' or 'archived'
    if (['inbox', 'archived'].includes(mailbox)) {
      // create archive button
      const archiveBtn = document.createElement('button');
      archiveBtn.innerHTML = `
        ${emailJSONContent.archived == true ? 
          `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive-fill" viewBox="0 0 16 16">
            <path d="M12.643 15C13.979 15 15 13.845 15 12.5V5H1v7.5C1 13.845 2.021 15 3.357 15h9.286zM5.5 7h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1zM.8 1a.8.8 0 0 0-.8.8V3a.8.8 0 0 0 .8.8h14.4A.8.8 0 0 0 16 3V1.8a.8.8 0 0 0-.8-.8H.8z"/>
          </svg>`
        : `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive" viewBox="0 0 16 16">
            <path d="M0 2a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1v7.5a2.5 2.5 0 0 1-2.5 2.5h-9A2.5 2.5 0 0 1 1 12.5V5a1 1 0 0 1-1-1V2zm2 3v7.5A1.5 1.5 0 0 0 3.5 14h9a1.5 1.5 0 0 0 1.5-1.5V5H2zm13-3H1v2h14V2zM5 7.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z"/>
          </svg>` 
        }
      `;
      archiveBtn.type = 'button';
      archiveBtn.className = 'btn btn-outline-secondary mt-2';
      archiveBtn.addEventListener('click', () => {
        // mark the email as archived
        fetch(`/emails/${emailJSONContent.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: emailJSONContent.archived == true ? false : true
          })
        });
        // load the specified mail
        load_mailbox('inbox');
      });

      // add tooltip to archive button
      archiveBtn.setAttribute('data-bs-toggle', 'tooltip');
      archiveBtn.setAttribute('data-bs-title', `${emailJSONContent.archived == true ? 'Unarchive' : 'Archive'}`);

      // add archive button to utilities div
      utilitiesDiv.append(archiveBtn);
    }

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
      <hr>
    `;

    email.append(emailContent);

    // apply CSS styling to email
    email.className = `
      list-group-item ${emailJSONContent.read == true ? 'text-muted' : ''}
      data-id="${emailJSONContent.id}"
    `;

    // create Core Functionalities div (to store core functionalities related buttons & functions)
    const coreFuncDiv = document.createElement('div');
    coreFuncDiv.className = `d-flex w-100`;

    // create Reply button
    const replyBtn = document.createElement('button');
    replyBtn.type = 'button';
    replyBtn.className = 'btn btn-outline-secondary mb-2';
    replyBtn.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-reply" viewBox="0 0 16 16">
        <path d="M6.598 5.013a.144.144 0 0 1 .202.134V6.3a.5.5 0 0 0 .5.5c.667 0 2.013.005 3.3.822.984.624 1.99 1.76 2.595 3.876-1.02-.983-2.185-1.516-3.205-1.799a8.74 8.74 0 0 0-1.921-.306 7.404 7.404 0 0 0-.798.008h-.013l-.005.001h-.001L7.3 9.9l-.05-.498a.5.5 0 0 0-.45.498v1.153c0 .108-.11.176-.202.134L2.614 8.254a.503.503 0 0 0-.042-.028.147.147 0 0 1 0-.252.499.499 0 0 0 .042-.028l3.984-2.933zM7.8 10.386c.068 0 .143.003.223.006.434.02 1.034.086 1.7.271 1.326.368 2.896 1.202 3.94 3.08a.5.5 0 0 0 .933-.305c-.464-3.71-1.886-5.662-3.46-6.66-1.245-.79-2.527-.942-3.336-.971v-.66a1.144 1.144 0 0 0-1.767-.96l-3.994 2.94a1.147 1.147 0 0 0 0 1.946l3.994 2.94a1.144 1.144 0 0 0 1.767-.96v-.667z"/>
      </svg>
      Reply
    `;

    replyBtn.addEventListener('click', () => {
      let recipient = emailJSONContent.sender;
      let subject = (emailJSONContent.subject.indexOf('Re') == 0) ? emailJSONContent.subject : 'Re: ' + emailJSONContent.subject ;
      let body = `On ${emailJSONContent.timestamp} ${emailJSONContent.sender} wrote: \n` + emailJSONContent.body;
      // execute compose_email()
      compose_email(cpRcpt=recipient, cpSbj = subject, cpBody=body);
    });

    // add Reply button to Core Functionalities div
    coreFuncDiv.append(replyBtn);

    // insert Core Functionalities div to email-view
    email.append(coreFuncDiv);

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
