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

    if (tweet.getElementsByClassName('tweetContent').length > 0) {
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
        if (jsonResponse['message'] == 'Tweet unliked successfully.') {
            // change like icon to un-liked
            const unLikedIcon = document.createElement('div');
            unLikedIcon.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="icon-image" viewBox="0 0 24 24">
                    <path d="M16.697 5.5c-1.222-.06-2.679.51-3.89 2.16l-.805 1.09-.806-1.09C9.984 6.01 8.526 5.44 7.304 5.5c-1.243.07-2.349.78-2.91 1.91-.552 1.12-.633 2.78.479 4.82 1.074 1.97 3.257 4.27 7.129 6.61 3.87-2.34 6.052-4.64 7.126-6.61 1.111-2.04 1.03-3.7.477-4.82-.561-1.13-1.666-1.84-2.908-1.91zm4.187 7.69c-1.351 2.48-4.001 5.12-8.379 7.67l-.503.3-.504-.3c-4.379-2.55-7.029-5.19-8.382-7.67-1.36-2.5-1.41-4.86-.514-6.67.887-1.79 2.647-2.91 4.601-3.01 1.651-.09 3.368.56 4.798 2.01 1.429-1.45 3.146-2.1 4.796-2.01 1.954.1 3.714 1.22 4.601 3.01.896 1.81.846 4.17-.514 6.67z"/>
                </svg>`;
            tweet.querySelector('#tweetLikeButton').innerHTML = unLikedIcon.outerHTML;
            // decrement Tweet likes
            var tweetLikes = tweet.querySelector('#tweet-likes').innerHTML;
            tweetLikes--;
            tweet.querySelector('#tweet-likes').innerHTML = tweetLikes;
        } else if (jsonResponse['message'] == 'Tweet liked successfully.') {
            // change like icon to liked
            const likedIcon = document.createElement('div');
            likedIcon.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#f91880" class="icon-image" viewBox="0 0 24 24">
                    <path d="M20.884 13.19c-1.351 2.48-4.001 5.12-8.379 7.67l-.503.3-.504-.3c-4.379-2.55-7.029-5.19-8.382-7.67-1.36-2.5-1.41-4.86-.514-6.67.887-1.79 2.647-2.91 4.601-3.01 1.651-.09 3.368.56 4.798 2.01 1.429-1.45 3.146-2.1 4.796-2.01 1.954.1 3.714 1.22 4.601 3.01.896 1.81.846 4.17-.514 6.67z"/>
                </svg>`;
            tweet.querySelector('#tweetLikeButton').innerHTML = likedIcon.outerHTML;
            // increment Tweet likes
            var tweetLikes = tweet.querySelector('#tweet-likes').innerHTML;
            tweetLikes++;
            tweet.querySelector('#tweet-likes').innerHTML = tweetLikes;
        } else {
            // error
        }
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

            // clear textarea of form
            document.querySelector('#tweetContent').value = '';

            // create new Tweet
            const tweet = jsonResponse["tweet"];
            let newTweet = document.querySelector(".tweet.user").cloneNode(true);
            newTweet.querySelector(".tweet-date").textContent = tweet.date;
            newTweet.querySelector(".tweet-content").textContent = tweet.content;
            newTweet.querySelector(".tweet-likes").textContent = tweet.likes;
            
            // add new Tweet to posts-view
            document.querySelector('#posts-view').prepend(newTweet);
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
