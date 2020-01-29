// Selecting elements
const messagesLink = document.getElementById("messages-link");
const notificationsLink = document.getElementById("notifications-link");
const generalModal = document.getElementById("general-modal");
const messageModal = document.getElementById("message-modal");
const messageForm = messageModal.querySelector(".message-form");

eventListeners();

function eventListeners(){
  messagesLink.addEventListener("click", e => {
    openDialogList();

    e.preventDefault();
  });

  generalModal.addEventListener("click", e => {
    if(e.target.id == "delete-dialog-button"){
      let dialog = e.target.parentElement.parentElement.parentElement;
      let uid = dialog.getAttribute("uid");

      if(confirm("Are you sure to delete this dialog? This is permanent!")){
        devSeater.deleteDialog(uid)
        .then(response => {
          if(response["ok"]){
            dialog.remove();
          }
        })
        .catch(err => console.error(err));
      }
    }

    e.preventDefault();
  });

  messageModal.querySelector(".modal-body").addEventListener("scroll", e => {
    if(e.target.scrollTop < 20){
      let mid = e.target.querySelector(".msg").getAttribute("mid");
      let uid = e.target.firstElementChild.getAttribute("uid");

      devSeater.dialogPreviousMessages(uid, mid)
      .then(response => {
        console.log(response["msgList"]);
        ui.showPreviousMessages(response["msgList"], Session.getCurrentUser());
      })
      .catch(err => console.error(err));
    }
  });

  messageForm.addEventListener("submit", e => {
    let uid = messageModal.querySelector(".modal-body").firstElementChild.getAttribute("uid");
    if(messageForm["message"].value != ""){
      sendMessage(uid, messageForm["message"].value);
    }
  });

  messageForm.querySelector("textarea").addEventListener("keydown", e => {
    if(e.keyCode === 13){
      let uid = messageModal.querySelector(".modal-body").firstElementChild.getAttribute("uid");
      if(messageForm["message"].value != ""){
        sendMessage(uid, messageForm["message"].value);
      }
    }
  });

}

function openMessageBox(uid){
  devSeater.dialogLastMessages(uid)
  .then(response => {
    devSeater.getUser(uid)
    .then(user => {
      console.log(response["msgList"]);
      ui.showMessages(response["msgList"], Session.getCurrentUser(), user);
    })
    .catch(err => console.error(err));
  })
  .catch(err => console.error(err));
}

function openDialogList(){
  devSeater.dialogList()
  .then(response => {
    ui.showDialogList(response["dialogList"]);
  })
  .catch(err => console.error(err));
}

function sendMessage(uid, message){
  devSeater.sendMessage({receiver_id : uid, text: message})
  .then(response => {
    if(response["result"] == "success"){
      ui.addMessage(response["mid"], message, "outgoing");
    }
  })
  .catch(err => console.error(err));
}