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
                        <small class="text-muted" id="tweet-likes">${tweetJSONContent.likes}</small>
                </div>
            `;

            // apply CSS styling to email
            tweet.className = `
                list-group-item list-group-item-action}
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
