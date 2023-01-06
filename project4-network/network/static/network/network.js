document.addEventListener('DOMContentLoaded', function() {

    // use buttons to toggle between views
    document.querySelector('#following').addEventListener('click', () => loadPostsFollowing());

    // create "New Post" functionality
    document.querySelector('#create-view').addEventListener('click', () => createPost());

    // load the "All Posts" section by default
    loadAllPosts();

});

function loadPostsAll() {
}

function loadPostsFollowing() {
}

function createPost() {
}
