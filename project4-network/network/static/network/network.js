document.addEventListener('DOMContentLoaded', function() {

    // use buttons to toggle between views
    document.querySelector('#following').addEventListener('click', () => loadPostsFollowing());

    // create "New Post" functionality
    document.querySelector('#create-view').addEventListener('click', () => createPost());

    // add Send Tweet functionality
    document.querySelector('#composeTweet').onsubmit = composeTweet;

    // load the "All Posts" section by default
    loadPostsAll();

});

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

function loadPostsAll() {

    // Set the class of posts-view
    document.querySelector('#posts-view').className = 'list-group';

    // Retrieve all posts
    fetch(`tweets`)
    .then(response => response.json())
    .then(tweets => {
        for (var key of Object.keys(tweets)) {
            const tweetJSONContent = tweets[key];
            console.log(tweetJSONContent);

            // create tweet HTML element
            let tweet = document.createElement('a');

            tweet.innerHTML = `
                <div class="d-flex w-100 justify-content-between">
                    <small class="text-muted" id="tweet-sender">${tweetJSONContent.user}</small>
                    <small class="text-muted" id="tweet-date">${tweetJSONContent.date}</small>
                </div>
                <div class="d-flex w-100 justify-content-between">
                    <span class="mb-1" id="tweet-content">${tweetJSONContent.content}</span>
                </div>
                <div>
                    <div>
                        <button type="button" id="likeBtn" class="btn btn-outline-primary mx-2 tweetBtns">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="icon-image" viewBox="0 0 24 24">
                                <path d="M16.697 5.5c-1.222-.06-2.679.51-3.89 2.16l-.805 1.09-.806-1.09C9.984 6.01 8.526 5.44 7.304 5.5c-1.243.07-2.349.78-2.91 1.91-.552 1.12-.633 2.78.479 4.82 1.074 1.97 3.257 4.27 7.129 6.61 3.87-2.34 6.052-4.64 7.126-6.61 1.111-2.04 1.03-3.7.477-4.82-.561-1.13-1.666-1.84-2.908-1.91zm4.187 7.69c-1.351 2.48-4.001 5.12-8.379 7.67l-.503.3-.504-.3c-4.379-2.55-7.029-5.19-8.382-7.67-1.36-2.5-1.41-4.86-.514-6.67.887-1.79 2.647-2.91 4.601-3.01 1.651-.09 3.368.56 4.798 2.01 1.429-1.45 3.146-2.1 4.796-2.01 1.954.1 3.714 1.22 4.601 3.01.896 1.81.846 4.17-.514 6.67z"/>
                            </svg>
                            </svg>
                        </button>
                        <small class="text-muted" id="tweet-likes">${tweetJSONContent.likes}</small>
                    </div>
                </div>
            `;

            // apply CSS styling to email
            tweet.className = `
                list-group-item list-group-item-action
            `;

            // append email HTML element to emails class
            document.querySelector('#posts-view').append(tweet);
        }
    })

}

function loadPostsFollowing() {
}

function createPost() {
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
