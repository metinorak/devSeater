//Selecting elements
const messageButton = document.querySelector(".message-button");
const userProfileCard = document.querySelector("#user-profile-card");

//Tabs
const postsButton = document.getElementById("posts-button");
const seatersButton = document.getElementById("seaters-button");
const skillsButton = document.getElementById("skills-button");
const aboutButton = document.getElementById("about-button");

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
      ui.clearContentArea();
      ui.showUserPosts(posts, Session.getCurrentUser());
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
				//Render markdown
				posts.forEach(post => {
					post["post"] = markDownConverter.makeHtml(post["post"]);
				});

				ui.showPreviousUserPosts(posts, Session.getCurrentUser());
			})
			.catch(err => console.error(err));
    }
	};
  
}