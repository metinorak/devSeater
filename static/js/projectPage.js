//Selecting elements
const postTextArea = document.getElementById("post-textarea");
const postButton = document.getElementById("post-button");
const projectProfileCard = document.getElementById("project-profile-card");
const pid = projectProfileCard.getAttribute("pid");

// Selecting tab buttons
const postsButton = document.getElementById("posts-button");
const seatersButton = document.getElementById("seaters-button");
const membersButton = document.getElementById("members-button");
const aboutButton = document.getElementById("about-button");

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
			devSeater.sendProjectPost(pid, simplemde.value().trim())
			.then(response => {
				if (response["result"] == "success"){
					ui.showPostAlert("success");
					simplemde.value("");
				}
			})
		});
	}

	postsButton.addEventListener("click", e => {
		devSeater.lastProjectPosts(pid)
		.then(posts => {
			ui.clearContentArea();
			ui.showPostTextAreaCard();
			ui.showPosts(posts, Session.getCurrentUser());
		})
		.catch(err => console.error(err));
	});
}