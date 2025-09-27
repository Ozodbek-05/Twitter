// Simulate login state
let isLoggedIn = false;
let currentUser = null;
let currentFilter = 'all';

// DOM Elements
const authSection = document.getElementById('auth-section');
const userSection = document.getElementById('user-section');
const postForm = document.getElementById('post-form');
const myPostsTab = document.getElementById('my-posts-tab');
const postsTitle = document.getElementById('posts-title');
const usernameDisplay = document.getElementById('username-display');

// Navigation
document.getElementById('posts-tab').addEventListener('click', function(e) {
    e.preventDefault();
    showAllPosts();
});

document.getElementById('my-posts-tab').addEventListener('click', function(e) {
    e.preventDefault();
    showMyPosts();
});

// Simulate login (you'll replace this with actual Django authentication)
document.addEventListener('DOMContentLoaded', function() {
    // Simulate user login for demo (remove this in production)
    setTimeout(() => {
        login('john_doe', 'John Doe');
    }, 1000);
});

function login(username, displayName) {
    isLoggedIn = true;
    currentUser = username;

    authSection.style.display = 'none';
    userSection.style.display = 'flex';
    postForm.style.display = 'block';
    myPostsTab.style.display = 'inline-block';
    usernameDisplay.textContent = displayName;

    updatePostActions();
}

function logout() {
    isLoggedIn = false;
    currentUser = null;

    authSection.style.display = 'flex';
    userSection.style.display = 'none';
    postForm.style.display = 'none';
    myPostsTab.style.display = 'none';

    hideAllEditForms();
    updatePostActions();
    showAllPosts();
}

document.getElementById('logout-btn').addEventListener('click', function(e) {
    e.preventDefault();
    logout();
});

// User filtering
document.querySelectorAll('.user-item').forEach(item => {
    item.addEventListener('click', function(e) {
        e.preventDefault();
        const user = this.dataset.user;
        filterPostsByUser(user);

        // Update active state
        document.querySelectorAll('.user-item').forEach(u => u.classList.remove('active'));
        this.classList.add('active');
    });
});

function filterPostsByUser(user) {
    currentFilter = user;
    const posts = document.querySelectorAll('.post-item');

    posts.forEach(post => {
        if (user === 'all' || post.dataset.user === user) {
            post.style.display = 'block';
        } else {
            post.style.display = 'none';
        }
    });

    updateTitle(user);
}

function showAllPosts() {
    currentFilter = 'all';
    filterPostsByUser('all');
    document.querySelector('.user-item[data-user="all"]').classList.add('active');
    document.querySelectorAll('.user-item:not([data-user="all"])').forEach(u => u.classList.remove('active'));
}

function showMyPosts() {
    if (currentUser) {
        currentFilter = currentUser;
        filterPostsByUser(currentUser);
        document.querySelectorAll('.user-item').forEach(u => u.classList.remove('active'));
        document.querySelector(`.user-item[data-user="${currentUser}"]`)?.classList.add('active');
    }
}

function updateTitle(user) {
    if (user === 'all') {
        postsTitle.textContent = 'All Posts';
    } else if (user === currentUser) {
        postsTitle.textContent = 'My Posts';
    } else {
        const userItem = document.querySelector(`.user-item[data-user="${user}"] h4`);
        const userName = userItem ? userItem.textContent : 'User';
        postsTitle.textContent = `${userName}'s Posts`;
    }
}

function updatePostActions() {
    const posts = document.querySelectorAll('.post-item');
    posts.forEach(post => {
        const actions = post.querySelector('.post-actions');
        if (isLoggedIn && post.dataset.user === currentUser) {
            actions.style.display = 'flex';
        } else {
            actions.style.display = 'none';
        }
    });
}

// Post editing functions
function editPost(postId) {
    hideAllEditForms();
    const editForm = document.getElementById(`edit-form-${postId}`);
    editForm.style.display = 'block';
}

function savePost(postId) {
    const editForm = document.getElementById(`edit-form-${postId}`);
    const textarea = editForm.querySelector('.edit-textarea');
    const postContent = document.querySelector(`[data-post-id="${postId}"] .post-content`);

    postContent.textContent = textarea.value;
    editForm.style.display = 'none';

    // Here you would send the update to your Django backend
    console.log('Saving post:', postId, textarea.value);
}

function deletePost(postId) {
    if (confirm('Are you sure you want to delete this post?')) {
        const post = document.querySelector(`[data-post-id="${postId}"]`);
        post.remove();

        // Here you would send the delete request to your Django backend
        console.log('Deleting post:', postId);
    }
}

function cancelEdit(postId) {
    const editForm = document.getElementById(`edit-form-${postId}`);
    editForm.style.display = 'none';
}

function hideAllEditForms() {
    document.querySelectorAll('.edit-form').forEach(form => {
        form.style.display = 'none';
    });
}

// Post creation
document.querySelector('.post-submit').addEventListener('click', function() {
    const textarea = document.querySelector('.post-textarea');
    const content = textarea.value.trim();

    if (content && isLoggedIn) {
        // Create new post element
        const newPostId = Date.now();
        const newPost = createPostElement(newPostId, currentUser, 'You', content, 'Just now');

        // Add to posts list
        const postsList = document.querySelector('.posts-list');
        postsList.insertBefore(newPost, postsList.firstChild);

        // Clear textarea
        textarea.value = '';

        // Update actions visibility
        updatePostActions();

        // Here you would send the new post to your Django backend
        console.log('Creating new post:', content);
    }
});

function createPostElement(postId, username, displayName, content, time) {
    const article = document.createElement('article');
    article.className = 'post-item';
    article.dataset.user = username;
    article.dataset.postId = postId;

    const initials = displayName.split(' ').map(n => n[0]).join('');

    article.innerHTML = `
        <div class="post-header">
            <div class="post-avatar">${initials}</div>
            <div class="post-user-info">
                <h4>${displayName}</h4>
                <span class="post-time">${time}</span>
            </div>
        </div>
        <div class="post-content">${content}</div>
        <div class="post-actions" style="display: none;">
            <button class="edit-btn" onclick="editPost(${postId})">Edit</button>
        </div>
        <div class="edit-form" id="edit-form-${postId}">
            <textarea class="edit-textarea">${content}</textarea>
            <div class="edit-actions">
                <button class="save-btn" onclick="savePost(${postId})">Save</button>
                <button class="delete-btn" onclick="deletePost(${postId})">Delete</button>
                <button class="cancel-btn" onclick="cancelEdit(${postId})">Cancel</button>
            </div>
        </div>
    `;

    return article;
}

// Initialize
showAllPosts();