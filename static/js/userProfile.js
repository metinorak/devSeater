//Selecting elements
const messageButton = document.querySelector(".message-button");
const userProfileCard = document.querySelector("#user-profile-card");

//Tabs
const postsButton = document.getElementById("posts-button");
const seatersButton = document.getElementById("seaters-button");
const skillsButton = document.getElementById("skills-button");

eventListeners();

function eventListeners(){

  userProfileCard.addEventListener("click", e => {
    
    if(e.target.classList.contains("follow-button")){
      let uid = e.target.parentElement.getAttribute("uid");

      if(e.target.classList.contains("followed")){
        //Unfollow the user
        devSeater.unFollow(uid)
        .then(response => {
          if(response["result"] == "success"){
            ui.unFollow(e.target);
          }
        })
        .catch(err => console.error(err));
      }
      else{
        //Follow the user
        devSeater.follow(uid)
        .then(response => {
          if(response["result"] == "success"){
            ui.follow(e.target);
          }
        })
        .catch(err => console.error(err));
      }

    }

  });

  postsButton.addEventListener("click", e => {
    let uid = userProfileCard.getAttribute("uid");

    devSeater.lastUserPosts(uid)
    .then(posts => {
      posts = renderPosts(posts);

      ui.clearContentArea();
      ui.showUserPosts(posts, Session.getCurrentUser());
      PR.prettyPrint();
    })
    .catch(err => console.error(err));

  });

  seatersButton.addEventListener("click", e => {
    let uid = userProfileCard.getAttribute("uid");

    devSeater.userSeaters(uid)
    .then(seaters => {
      ui.clearContentArea();
      ui.showUserSeaters(seaters);
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

        ui.showPreviousUserPosts(posts, Session.getCurrentUser());
        PR.prettyPrint();
			})
			.catch(err => console.error(err));
    }
	};
  
}
