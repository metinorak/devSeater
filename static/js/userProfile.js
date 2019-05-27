//Selecting elements
const messageButton = document.querySelector(".message-button");
const followButton = document.querySelector(".follow-button");
const userProfileCard = document.querySelector("#user-profile-card");

//Tabs
const postsButton = document.getElementById("posts-button");
const seatersButton = document.getElementById("seaters-button");
const skillsButton = document.getElementById("skills-button");

eventListeners();

function eventListeners(){
  document.addEventListener("DOMContentLoaded", e => {
    let uid = userProfileCard.getAttribute("uid");
    if(Session.getCurrentUser()["uid"] == uid){
      messageButton.style.display = "none";
      followButton.style.display = "none";
    }
  });

  postsButton.addEventListener("click", e => {
    let uid = userProfileCard.getAttribute("uid");

    devSeater.lastUserPosts(uid)
    .then(posts => {
      posts = renderPosts(posts);

      ui.clearContentArea();
      ui.showPosts(posts, Session.getCurrentUser());
      PR.prettyPrint();
    })
    .catch(err => console.error(err));

  });

  seatersButton.addEventListener("click", e => {
    let uid = userProfileCard.getAttribute("uid");

    devSeater.userSeaters(uid)
    .then(seaters => {
      ui.clearContentArea();
      ui.showSeaters(seaters);
    })
    .catch(err => console.error(err));
  });

  skillsButton.addEventListener("click", e => {
    let uid = userProfileCard.getAttribute("uid");

    devSeater.userSkills(uid)
    .then(skills => {
      ui.clearContentArea();
      ui.showUserSkills(skills);
    })
    .catch(err => console.error(err));
  });

	//When touched the bottom
	window.onscroll = function(e) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
			// Load previous following posts
			let lastPost = getTheLastPost();
      let upid = lastPost.getAttribute("upid");
      let uid = userProfileCard.getAttribute("uid");

			devSeater.previousUserPosts(uid, upid)
			.then(posts => {
				posts = renderPosts(posts);

        ui.showPreviousPosts(posts, Session.getCurrentUser());
        PR.prettyPrint();
			})
			.catch(err => console.error(err));
    }
	};
  
}
