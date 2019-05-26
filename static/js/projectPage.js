//Selecting elements
const postTextArea = document.getElementById("post-textarea");
const postButton = document.getElementById("post-button");
const projectProfileCard = document.getElementById("project-profile-card");

//SIMPLEMDE textarea control
if(postTextArea != null){
	var simplemde = new SimpleMDE({
		element: postTextArea,
		showIcons: ["code"],
		hideIcons: ["side-by-side", "fullscreen"],
		spellChecker: false
	
	});
}

eventListeners();

function eventListeners(){
  
  if(postButton != null){
		postButton.addEventListener('click', e => {
      let pid = projectProfileCard.getAttribute("pid");

			devSeater.sendProjectPost(pid, simplemde.value().trim())
			.then(response => {
				if (response["result"] == "success"){
					ui.showPostAlert("success");
					simplemde.value("");
				}
			})
		});
	}
}