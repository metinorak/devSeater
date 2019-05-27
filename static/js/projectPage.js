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

	document.addEventListener("DOMContentLoaded", e => {
		devSeater.isProjectMember(pid, Session.getCurrentUser()["uid"])
		.then(response => {
			if(response["result"]){
				ui.showPostTextAreaCard();
			}
		})
		.catch(err => console.error(err));
	});
  
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

	seatersButton.addEventListener("click", e => {
		devSeater.projectEmptySeaters(pid)
		.then(seaters => {
			ui.clearContentArea();
			ui.hidePostTextAreaCard();
			ui.showEmptySeaters(seaters);
		})
		.catch(err => console.error(err));
	});

	document.addEventListener("click", e => {
		if(e.target.id == "empty-seaters"){
			devSeater.projectEmptySeaters(pid)
			.then(seaters => {
				ui.clearContentArea();
				ui.hidePostTextAreaCard();
				ui.showEmptySeaters(seaters);
			})
			.catch(err => console.error(err));

			e.preventDefault();
		}

		if(e.target.id == "filled-seaters"){
			devSeater.projectFilledSeaters(pid)
			.then(seaters => {
				ui.clearContentArea();
				ui.hidePostTextAreaCard();
				ui.showFilledSeaters(seaters);
			})
			.catch(err => console.error(err));

			e.preventDefault();
		}


	});

}