//Selecting elements
const postTextArea = document.getElementById("post-textarea");
const postButton = document.getElementById("post-button");
const projectProfileCard = document.getElementById("project-profile-card");
const pid = projectProfileCard.getAttribute("pid");
const contentArea = document.querySelector(".content-area");
const projectNameInfo = document.querySelector("#project-name-info");
const projectShortDescriptionInfo = document.querySelector("#project-short-description-info");

// Selecting tab buttons
const postsButton = document.getElementById("posts-button");
const seatersButton = document.getElementById("seaters-button");
const membersButton = document.getElementById("members-button");
const aboutButton = document.getElementById("about-button");
const membersLink = document.getElementById("members-link");
const editProjectButton = document.querySelector("#edit-project-button");

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

		devSeater.isProjectAdmin(pid, Session.getCurrentUser()["uid"])
		.then(response => {
			if(response["result"]){
				editProjectButton.style.display = "inline";
			}
		})
		.catch(err => console.error(err));

	});

	membersButton.addEventListener("click", e=>{
		devSeater.projectMembers(pid)
		.then(members => {
			ui.hidePostTextAreaCard();
			ui.clearContentArea();
			ui.showProjectMembers(members, Session.getCurrentUser());
		})
		.catch(err => console.error(err));
	});

	membersLink.addEventListener("click", e => {
		devSeater.projectMembers(pid)
		.then(members => {
			ui.hidePostTextAreaCard();
			ui.clearContentArea();
			ui.showProjectMembers(members, Session.getCurrentUser());
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

	aboutButton.addEventListener("click", e => {
		devSeater.project(pid)
		.then(pr => {
			let text = renderText(pr["full_description"]);
			ui.clearContentArea();
			ui.hidePostTextAreaCard();
			ui.showAboutText(text);
		})
		.catch(err => console.error(err));
	});

	editProjectButton.addEventListener("click", e => {

    Promise.all([devSeater.project(pid), devSeater.projectLinks(pid)])
    .then(values => {
			ui.clearContentArea();
			ui.hidePostTextAreaCard();
      ui.showProjectPageSettings(...values, mde => {
				var fullDescriptionInput = mde;

				//Add event to the fullDescriptionInput
				fullDescriptionInput.codemirror.on("blur", e => {
					let element = fullDescriptionInput.element;
					devSeater.updateProjectFullDescription(fullDescriptionInput.value())
					.then(response => {
						if(response["result"] == "success"){
							ui.showMessageAfterElement(element, "Full description updated!", "success");
						}
						else{
							ui.showMessageAfterElement(element, "Full description couldn't be updated!", "fail");
						}
					})
					.catch(err => console.error(err));

				});
			
			});
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

  //Project page settings events
  contentArea.addEventListener("change", e => {
    if(e.target.id == "project-photo"){
      let file, img;

      if ((file = e.target.files[0])) {
          img = new Image();
          img.onload = function() {
              let ratio = this.width / this.height;
              if(ratio == (16/9)){
                ui.showMessageAfterElement(e.target, "File is uploading...", "info");
                devSeater.updateProjectPhoto(pid, file)
                .then(response => {
									console.log(response);
									if(response["result"] == "success")
                    ui.showMessageAfterElement(e.target, "File uploaded!", "success");
                  else
                    ui.showMessageAfterElement(e.target, response["msg"], "fail");
                })
                .catch(err => console.error(err));
              }
              else{
                alert("The file is not in the desired ratio! (16:9)");
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
    if(e.target.id == "project-name"){
      devSeater.updateProjectName(pid, e.target.value)
      .then(response => {
        if(response["result"] == "success"){
          ui.showMessageAfterElement(e.target, "Project name updated!", "success");
          projectNameInfo.textContent = e.target.value;
        }
        else{
          ui.showMessageAfterElement(e.target, "Project name couldn't be updated!", "fail");
        }
      })
      .catch(err => console.error(err));
    }
    else if(e.target.id == "project-short-description"){
      devSeater.updateProjectShortDescription(e.target.value)
      .then(response => {
        if(response["result"] == "success"){
          ui.showMessageAfterElement(e.target, "Short description updated!", "success");
          projectShortDescriptionInfo.textContent = e.target.value;
        }
        else{
          ui.showMessageAfterElement(e.target, "Short description couldn't be updated!", "fail");
        }
      })
      .catch(err => console.error(err));
		}
	});
	
  contentArea.addEventListener("click", e => {
		if(e.target.id == "create-a-new-seater"){
			ui.getSeaterFromUser()
			.then(seater => {
				devSeater.createSeater(pid, seater)
				.then(response => {
					if(response["result"] == "success"){
						redirect(`/p/${projectNameInfo.textContent}/seaters/${response["sid"]}`);
					}
				})	
				.catch(err => console.error(err));
			})
			.catch(err => console.error(err));
		}

    if(e.target.id == "add-new-link"){
      ui.getNewLinkFromUser()
      .then(link => {
				let linkList = e.target.previousElementSibling.firstElementChild;
        devSeater.addProjectLink(pid, link)
        .then(response => {
          if(response["result"] == "success"){
            link["plid"] = response["plid"];
            ui.addLinkListItem(link, linkList);
          }
        })
        .catch(err => console.log(err));
      })
      .catch(err => console.error(err));

      e.preventDefault();
    }
    else if(e.target.id == "delete-project-link"){
      if (confirm("Are you sure to delete this link?")){
        let plid = e.target.parentElement.getAttribute("plid");

        devSeater.deleteProjectLink(plid)
        .then(response => {
					if(response["ok"])
          	e.target.parentElement.remove();
        })
        .catch(err => console.error(err));
      }
      e.preventDefault();
    }
  });
}