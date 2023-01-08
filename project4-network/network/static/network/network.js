document.addEventListener('DOMContentLoaded', function() {

    // use buttons to toggle between views
    document.querySelector('#following').addEventListener('click', () => loadPostsFollowing());

    // create "New Post" functionality
    document.querySelector('#create-view').addEventListener('click', () => createPost());

    // add Send Tweet functionality
    document.querySelector('#composeTweet').onsubmit = composeTweet;

    // load the "All Posts" section by default
    loadAllPosts();

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
    .then(
        console.log("success!")
    )

    return false;
}

function loadPostsAll() {
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
