//Selecting elements
const messageButton = document.querySelector(".message-button");
const followButton = document.querySelector(".follow-button");
const userProfileCard = document.querySelector("#user-profile-card");
const contentArea = document.querySelector(".content-area");
const userFullNameInfo = document.querySelector(".user-full-name-info");
const userBioInfo = document.querySelector(".user-bio-info");

//Tabs
const postsButton = document.getElementById("posts-button");
const seatersButton = document.getElementById("seaters-button");
const skillsButton = document.getElementById("skills-button");
const editProfileButton = document.getElementById("edit-profile-button");

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

  editProfileButton.addEventListener("click", e => {

    Promise.all([devSeater.currentUser(), devSeater.userLinks(), devSeater.userSkills()])
    .then(values => {
      ui.clearContentArea();
      ui.showUserProfileSettings(...values);
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
  
  //Profile settings events
  contentArea.addEventListener("change", e => {
    if(e.target.id == "profile-photo"){
      let file, img;

      if ((file = e.target.files[0])) {
          img = new Image();
          img.onload = function() {
              let ratio = this.width / this.height;
              if(ratio >= 0.99 && ratio <= 1.01){
                ui.showMessageAfterElement(e.target, "File is uploading...", "info");
                devSeater.updateUserPhoto(null, file)
                .then(response => {
                  if(response["result"] == "success")
                    ui.showMessageAfterElement(e.target, "File uploaded!", "success");
                  else
                    ui.showMessageAfterElement(e.target, response["msg"], "fail");
                })
                .catch(err => console.error(err));
              }
              else{
                alert("The file is not in the desired ratio!");
              }
          };
          img.onerror = function() {
              alert( "not a valid file: " + file.type);
          };
          img.src = URL.createObjectURL(file);
      }
  
    }

  });

  contentArea.addEventListener("focusout", e => {
    if(e.target.id == "user-full-name"){
      devSeater.updateUserFullName(e.target.value)
      .then(response => {
        if(response["result"] == "success"){
          ui.showMessageAfterElement(e.target, "Full name updated!", "success");
          userFullNameInfo.textContent = e.target.value;
        }
        else{
          ui.showMessageAfterElement(e.target, "Full name couldn't be updated!", "fail");
        }
      })
      .catch(err => console.error(err));
    }
    else if(e.target.id == "user-bio"){
      devSeater.updateUserBio(e.target.value)
      .then(response => {
        if(response["result"] == "success"){
          ui.showMessageAfterElement(e.target, "Bio updated!", "success");
          userBioInfo.textContent = e.target.value;
        }
        else{
          ui.showMessageAfterElement(e.target, "Bio couldn't be updated!", "fail");
        }
      })
      .catch(err => console.error(err));
    }
  });

  contentArea.addEventListener("click", e => {

    if(e.target.id == "add-new-link"){
      
    }
    else if(e.target.classList.contains("delete-user-link")){

    }
    else if(e.target.classList.contains("delete-user-skill")){

    }
    else if(e.target.id == "add-new-skill"){

    }

  });
  
}

function addNewLinkInput(e){
  ui.addAnotherLinkInput(e.target.previousElementSibling);
  e.preventDefault();
}
