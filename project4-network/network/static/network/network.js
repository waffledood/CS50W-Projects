document.addEventListener('DOMContentLoaded', function() {

    // add Send Tweet functionality
    document.querySelector('#composeTweet').onsubmit = composeTweet;

    // edit button on Tweet 
    document.querySelectorAll('.editBtn').forEach(editBtn => {
        editBtn.addEventListener('click', (event) => editButton(event));
    });

    // like button on Tweet 
    document.querySelectorAll('.likeBtn').forEach(likeBtn => {
        likeBtn.addEventListener('click', (event) => likeButton(event));
    });

});

function editButton(event) {
    console.log(event.target);
    console.log(event.currentTarget);
    // attach event listener to div
    // event.currentTarget.addEventListener('click', );

    // get the parent tweet div
    let tweet = event.target.closest('.tweet');

    const tweetContentDiv = tweet.querySelector('.tweetContentDiv');

    // retrieve tweet content
    const tweetContent = tweet.querySelector('.tweetContent');

    // remove contents of tweetContentDiv
    tweetContentDiv.innerHTML = '';

    // insert textarea to tweetContentDiv
    const tweetContentEdit = document.createElement('textarea');
    tweetContentEdit.className = 'tweetContentEdit';
    tweetContentEdit.innerHTML = tweetContent.innerHTML;
    tweetContentDiv.append(tweetContentEdit);

    // create Save button
    const saveButton = document.createElement('button');
    saveButton.innerHTML = 'Save';
    saveButton.className ='btn btn-outline-primary';
    saveButton.addEventListener('click', () => {
        const tweetContentEditNew = tweetContentDiv.querySelector('.tweetContentEdit').value;

        if (tweetContentEditNew.length == 0) {
            console.log("empty!");
        } else {
            // submit edited Tweet to API
            let csrftoken = getCookie('csrftoken');
            fetch(`/editTweet/${tweet.dataset.id}`, {
                method: 'PATCH',
                body: JSON.stringify({
                    editedTweetContent: tweetContentEditNew
                }),
                headers: { "X-CSRFToken": csrftoken }
            })
            .then(response => response.json())
            .then(jsonResponse => {
                // remove contents of tweetContentDiv
                tweetContentDiv.innerHTML = '';
            
                // create span element with newly edited Tweet content
                const tweetContentEditNewSpan = document.createElement('span');
                tweetContentEditNewSpan.className = 'tweetContent';
                tweetContentEditNewSpan.innerText = tweetContentEditNew;
                tweetContentDiv.append(tweetContentEditNewSpan);
            })
        }
    });

    // add Save button to tweet
    tweetContentDiv.append(saveButton);
}

function likeButton(event) {
    // get the parent tweet div
    let tweet = event.target.closest('.tweet');

    // call likeTweet API
    let csrftoken = getCookie('csrftoken');
    fetch(`/likeTweet`, {
        method: 'POST',
        body: JSON.stringify({
            idTweetLiked: tweet.dataset.id
        }),
        headers: { "X-CSRFToken": csrftoken }
    })
    .then(response => response.json())
    .then(jsonResponse => {
        console.log(jsonResponse);
    })
}

function composeTweet() {
    // retrieve email contents from form
    const tweetContent = document.querySelector('#tweetContent').value;

    let csrftoken = getCookie('csrftoken');

    // submit the POST request to send an email
    fetch('/tweet', {
        method: 'POST',
        body: JSON.stringify({
            tweetContent: tweetContent
        }),
        headers: { "X-CSRFToken": csrftoken }
    })
    .then(response => response.json())
    .then(jsonResponse => {
        if ("message" in jsonResponse) {
            // success message
            const successMsg = jsonResponse["message"];
            console.log(successMsg);
            // TODO - add handling for success
        } else {
            // error message
            const errMsg = jsonResponse["error"];
            console.log(errMsg);
            // TODO - add handling for error
        }
    })

    return false;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function enablePopovers() {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
}
