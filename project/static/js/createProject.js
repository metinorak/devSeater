// Selecting elements
const addAnotherLinkButton = document.getElementById("add-another-link-button");
const fullDescriptionInput = document.getElementsByName("full-description")[0];

//SIMPLEMDE textarea control

if(fullDescriptionInput != null){
	var simplemde = new SimpleMDE({
		element: fullDescriptionInput,
		showIcons: ["code"],
		hideIcons: ["side-by-side", "fullscreen"],
		spellChecker: false
	
	});
}

eventListeners();

function eventListeners(){

	if(addAnotherLinkButton != null){
		addAnotherLinkButton.addEventListener("click", e => {
			ui.addAnotherLinkInputToTheCreateProjectPage();
		});
	}
}