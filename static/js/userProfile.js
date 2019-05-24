//Selecting elements
const messageButton = document.querySelector(".message-button");
const userProfileCard = document.querySelector("#user-profile-card");


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
}