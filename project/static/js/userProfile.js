//Selecting elements
const messageButton = document.querySelector(".message-button");
const followButton = document.querySelector(".follow-button");
const newProjectButton = document.querySelector(".new-project-button");
const userProfileCard = document.querySelector("#user-profile-card");
const uid = userProfileCard.getAttribute("uid");
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
    if(!Session.isLoggedIn() || Session.getCurrentUser()["uid"] == uid){
      messageButton.style.display = "none";
      followButton.style.display = "none";
    }

    if(uid == Session.getCurrentUser()["uid"]){
      editProfileButton.style.display = "inline";
      newProjectButton.style.display = "inline";
    }
  });

  messageButton.addEventListener("click", e => {
    openMessageBox(uid);
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

      if(lastPost != undefined){
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
                ui.showMessageAfterElement(e.target, "Uploading file...", "info");
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

  contentArea.addEventListener("change", e => {
    if(e.target.id == "user-full-name"){
      devSeater.updateUserFullName(e.target.value)
      .then(response => {
        if(response["result"] == "success"){
          ui.showMessageAfterElement(e.target, "Full name updated!", "success");
          userFullNameInfo.textContent = e.target.value;
          ui.changeFullNameInNavbar(e.target.value);
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
      ui.getNewLinkFromUser()
      .then(link => {
        let linkList = e.target.previousElementSibling.firstElementChild;
        devSeater.addUserLink(link)
        .then(response => {
          if(response["result"] == "success"){
            link["ulid"] = response["ulid"];
            ui.addLinkListItem(link, linkList);
          }
        })
        .catch(err => console.log(err));
      })
      .catch(err => console.error(err));

      e.preventDefault();
    }
    else if(e.target.id == "delete-user-link"){
      if (confirm("Are you sure to delete this link?")){
        let ulid = e.target.parentElement.getAttribute("ulid");

        devSeater.deleteUserLink(ulid)
        .then(response => {
          e.target.parentElement.remove();
        })
        .catch(err => console.error(err));
      }
      

      e.preventDefault();
    }
    else if(e.target.classList.contains("delete-user-skill")){
      let skid = e.target.parentElement.getAttribute("skid");

      if(confirm("Are you sure to delete this skill?")){
        devSeater.deleteUserSkill(skid)
        .then(response => {
          if(response["ok"]){
            e.target.parentElement.remove();
          }
        })
        .catch(err => console.log(err));
      }
      e.preventDefault();
    }
    else if(e.target.id == "add-new-skill"){
      ui.getNewSkillFromUser()
      .then(skill => {
        let skillList = e.target.previousElementSibling.firstElementChild;
        devSeater.addUserSkill(skill)
        .then(response => {
          if(response["result"] == "success"){
            let skid = response["skid"];
            let skillElement = {name: skill, skid: skid};
            ui.addSkillListItem(skillElement, skillList);
          }
        })
        .catch(err => console.log(err));
      })
      .catch(err => console.log(err));

      e.preventDefault();
    }

  });
  
}
