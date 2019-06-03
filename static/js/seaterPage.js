//Selecting elements
const aspireButton = document.getElementById("aspire-button");
const dismissUserButton = document.getElementById("dismiss-user-button");
const removeSeaterButton = document.getElementById("remove-seater-button");
const aspirationsListButton = document.getElementById("aspirations-list-button");
const cancelAspirationButton = document.getElementById("cancel-aspiration-button");
const seaterPageCard = document.querySelector(".card");
const sid = seaterPageCard.getAttribute("sid");
const pid = seaterPageCard.getAttribute("pid");
const projectName = seaterPageCard.getAttribute("project-name");

eventListeners();

function eventListeners(){
  if(aspireButton != null){
    aspireButton.addEventListener("click", e => {
      devSeater.aspireSeater(sid)
      .then(response => {
        if(response["result"] == "success"){
          location.reload();
        }
      })
      .catch(err => console.error(err));
    });
  }

  if(cancelAspirationButton != null){
    cancelAspirationButton.addEventListener("click", e => {
      devSeater.cancelSeaterAspiration(sid)
      .then(response => {
        if(response["result"] == "success"){
          location.reload();
        }
      })
      .catch(err => console.error(err));
    });
  }
  
  if(dismissUserButton != null){
    dismissUserButton.addEventListener("click", e => {
      devSeater.dismissUserToTheSeater(sid)
      .then(response => {
        if(response["result"] == "success")
          location.reload();
      })
      .catch(err => console.error(err));
    });
  }

  if(removeSeaterButton != null){
    removeSeaterButton.addEventListener("click", e => {
      devSeater.removeSeater(sid)
      .then(response => {
        if(response["ok"])
          redirect(`/p/${projectName}`);  
      })
      .catch(err => console.error(err));
    });
  }

  if(aspirationsListButton != null){

  }

}