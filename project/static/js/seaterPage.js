//Selecting elements
const aspireButton = document.getElementById("aspire-button");
const dismissUserButton = document.getElementById("dismiss-user-button");
const removeSeaterButton = document.getElementById("remove-seater-button");
const editSeaterButton = document.getElementById("edit-seater-button");
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
      if(confirm("Are you sure to delete this seater? This is permanent!")){
        devSeater.removeSeater(sid)
        .then(response => {
          if(response["ok"])
            redirect(`/p/${projectName}`);  
        })
        .catch(err => console.error(err));
      }
    });
  }

  if(editSeaterButton != null){
    editSeaterButton.addEventListener("click", e => {
      devSeater.seater(sid)
      .then(async (seater) => {
        seater = await ui.getSeaterFromUser(seater);
        seater["sid"] = sid;

        devSeater.updateSeater(pid, seater)
        .then(response => {
            if(response["result"] == "success"){
              location.reload();
            }
        })
        .catch(err => console.error(err));
      })
      .catch(err => console.error(err));

    });
  }

  if(aspirationsListButton != null){
    aspirationsListButton.addEventListener("click", e=>{
      devSeater.seaterAspirations(sid)
      .then(aspirations => {
        ui.showSeaterAspirationsList(aspirations);
      })
      .catch(err => console.error(err));
    });
  }

  document.addEventListener("click", e=>{
    if(e.target.id == "assign-user-button"){
      let element = e.target.parentElement.parentElement.parentElement;
      let sid = element.getAttribute("sid");
      let uid = element.getAttribute("uid");

      devSeater.assignUserToTheSeater(sid, uid)
      .then(response => {
        if(response["result"] == "success"){
          location.reload();
        }
      })
      .catch(err => console.error(err));
    }
    else if(e.target.id == "reject-user-button"){
      if(confirm("Are you sure to reject this user? This is permanent!")){
        let element = e.target.parentElement.parentElement.parentElement;
        let sid = element.getAttribute("sid");
        let uid = element.getAttribute("uid");
  
        devSeater.rejectSeaterAspiration(sid, uid)
        .then(response => {
          if(response["result"] == "success"){
            element.remove();
            devSeater.seaterAspirationNumber(sid)
            .then(response => {
              if(response["number"] == 0){
                ui.hideGeneralModal();
              }
            })
          }
        })
        .catch(err => console.error(err));
      }
    }
  });

}