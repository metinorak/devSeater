// Selecting elements
const usernameUpdateForm = document.getElementById("update-username");
const emailUpdateForm = document.getElementById("update-email");
const passwordUpdateForm = document.getElementById("update-password")


eventListeners();

function eventListeners(){
  usernameUpdateForm["username"].addEventListener("input", e => {
    //Validate username
    if(!isValidUsername(e.target.value)){
      ui.showMessageAfterElement(e.target, 
        "Username is not valid! It should be at least 1 character alpha-numeric and can contain '-', '_'",
        "fail");
    }
    else{
      //Check username availability
      devSeater.checkUsernameAvailability(e.target.value)
      .then(response => {
        if(response["result"]){
          ui.showMessageAfterElement(e.target, "Username is available!", "success");
        }
        else{
          ui.showMessageAfterElement(e.target, "Username is not available!", "fail");
        }
      })
      .catch(err => console.error(err));
    }
  });

  passwordUpdateForm["new-password"].addEventListener("input", e => {
    //Validate password
    if(!isValidPassword(e.target.value)){
      ui.showMessageAfterElement(e.target, "Password is not valid! It should be at least 6 characters.", "fail");
    }
    else{
      ui.showMessageAfterElement(e.target, "");
    }

  });

  passwordUpdateForm["confirm-new-password"].addEventListener("input", e => {
    //Check if passwords match
    if(passwordUpdateForm["new-password"].value != passwordUpdateForm["confirm-new-password"].value){
      ui.showMessageAfterElement(e.target, "Passwords do not match!", "fail");
    }
    else{
      ui.showMessageAfterElement(e.target, "");
    }

  });

	usernameUpdateForm.addEventListener("submit", e => {
    devSeater.updateUsername({
      username: e.target["username"].value,
      password: e.target["password"].value
    })
    .then(response => {
      if(response["result"] == "success"){
        ui.showAlert(e.target, response["msg"], "success", "beforebegin");
        ui.changeUsernameInNavbar(e.target["username"].value);
      }
      else{
        ui.showAlert(e.target, response["msg"], "danger", "beforebegin");
      }
    })
    .catch(err => console.error(err));
    e.preventDefault();
  });

  emailUpdateForm.addEventListener("submit", e => {
    devSeater.updateEmail({
      email: e.target["email"].value,
      password: e.target["password"].value
    })
    .then(response => {
      if(response["result"] == "success"){
        ui.showAlert(e.target, response["msg"], "success", "beforebegin");
      }
      else{
        ui.showAlert(e.target, response["msg"], "danger", "beforebegin");
      }
    })
    .catch(err => console.error(err));
    e.preventDefault();
  });

  passwordUpdateForm.addEventListener("submit", e => {
    devSeater.updatePassword({
      currentPassword: e.target["current-password"].value,
      newPassword: e.target["new-password"].value,
      confirmNewPassword: e.target["confirm-new-password"].value
    })
    .then(response => {
      if(response["result"] == "success"){
        ui.showAlert(e.target, response["msg"], "success", "beforebegin");
      }
      else{
        ui.showAlert(e.target, response["msg"], "danger", "beforebegin");
      }
    })
    .catch(err => console.error(err));

    e.preventDefault();
  })
}

function isValidUsername(username){
  if(username.match(/^[a-zA-Z0-9-_]+$/) == null){
    return false;
  }
  return true;
}

function isValidPassword(password){
  if(password.length < 6){
    return false;
  }
  return true;
}
