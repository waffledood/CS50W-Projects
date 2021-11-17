document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // When User sends an email
  //document.querySelector('#compose-form').addEventListener('submit', send_email);
  document.querySelector('#compose-form').onsubmit = send_email;

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#email-entry-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block'; 

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function reply_email(email) {
  
  // Show compose view and hide other views
  document.querySelector('#email-entry-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Pre-fill composition fields
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = email.subject.includes("Re:") ? email.subject : "Re: " + email.subject;
  const body_text = "On " + email.timestamp + " " + email.sender + " wrote: \n" + email.body;
  document.querySelector('#compose-body').value = body_text;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-entry-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      //console.log(emails);

      //emails.forEach(function(item) {
      emails.forEach(item => {
        const email_entry = document.createElement('div');

        // Email entry contents
          // Sender
          const sender = document.createElement('div');
          sender.innerHTML = item.sender;

          // Email content
          const email_content = document.createElement('div');
          email_content.innerHTML = item.body;

          // Email timestamp
          const timestamp = document.createElement('div');
          timestamp.innerHTML = item.timestamp;

        // Finalized Email Entry
        //email_entry = sender + email_content + timestamp;
        email_entry.innerHTML = item.sender + ", " + item.body + ", " + item.timestamp;

        // Email entry formatting
        email_entry.style.border = "medium groove #2C3E50";
        email_entry.style.borderRadius = "5px";
        email_entry.style.cursor = "pointer"
          // If email has been read, its background is white, else it's grey
          if (item.read) {
            email_entry.style.backgroundColor = "#FDFEFE";
          } else {
            email_entry.style.backgroundColor = "#99A3A4";
          }
        
        // Viewing Email functionality
        email_entry.addEventListener('click', () => view_email(item, mailbox));

        document.querySelector('#emails-view').append(email_entry);
      });
      
  });

  return false;
}

function view_email(email, mailbox) {

  // Hide other views (mailbox, sent, compose, archive)
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-entry-view').style.display = 'block';

  // Clear out previous loaded email
  document.querySelector('#email-entry-view').innerHTML = '';
    //document.querySelector('#email-entry-view').value = '';

  // Contents of email entry
  const email_entry = document.createElement('div');
  email_entry.innerHTML += "<div>" + "From: " + email.sender + "</div>";
  email_entry.innerHTML += "<div>" + "To: " + email.recipients.join(',') + "</div>";
  email_entry.innerHTML += "<div>" + "Subject: " + email.subject + "</div>";
  email_entry.innerHTML += "<div>" + "Timestamp: " + email.timestamp + "</div>";
  email_entry.innerHTML += "<hr>";
  email_entry.innerHTML += email.body;

  // Adding the Email content
  document.querySelector('#email-entry-view').append(email_entry);

  // Archive / Unarchive functionality only applies for all mailboxes except 'Sent'
  if (mailbox !== 'sent') {
    // Archive / Unarchive button 
    const archive_button = document.createElement('button');
    archive_button.className = "btn btn-sm btn-outline-primary";

    // Format the Archive / Unarchive button accordingly & load the Archive/Unarchive functionality
    if (email.archived) {
      archive_button.innerHTML = "Unarchive";
      archive_button.addEventListener('click', () => archive_email(email.id, false));
    } else {
      archive_button.innerHTML = "Archive";
      archive_button.addEventListener('click', () => archive_email(email.id, true));
    } 

    // Mark the email as read
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })

    // Adding the Archive button
    document.querySelector('#email-entry-view').append(archive_button);
  }

  // Adding the Reply button
  const reply_button = document.createElement("button");
  reply_button.className = "btn btn-sm btn-outline-primary";
  reply_button.innerHTML = "Reply";
  reply_button.addEventListener('click', () => reply_email(email));
  document.querySelector('#email-entry-view').append(reply_button);

}

function archive_email(email_id, bool_archive) {

  // Archive / Unarchive the specified email
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: bool_archive
    })
  })
  //.then(result => console.log(result))
  //.then(setTimeout(load_mailbox('inbox'), 2000));
  .then(load_mailbox('inbox'));

  console.log("Email, " + bool_archive + ": " + email_id);
}

function send_email() {
  
  // Send the email with its relevant contents 
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);

      if (result.error) {
        document.querySelector('#compose-view').value = '';
        const alert = document.createElement('div');
        alert.innerHTML = 'Error!';
        alert.className = "alert alert-danger";
        document.querySelector('#compose-view').append(alert);
      } else {
        load_mailbox('sent');
      }
  });

  return false;
}
