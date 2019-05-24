//Selecting elements
const memberOptions = document.getElementById("member-options");
const navbarLinks = document.getElementById("navbar-links");
const searchInput = document.getElementById("search-input");
const searhResults = document.getElementById("search-results");
const searchForm = document.getElementById("search-form");
const timeInfos = document.querySelectorAll(".time");

const ui = new UI();
const devSeater = new DevSeater();

//RENDER MARKDOWN
const markDownConverter = new showdown.Converter({extensions: ['prettify']});
document.querySelectorAll(".post-body").forEach(post => {
	post.innerHTML = markDownConverter.makeHtml(post.textContent.trim());
});

// Time info type changing
ui.changeTimeFormats(timeInfos);

eventListeners();

function eventListeners(){

	document.addEventListener("DOMContentLoaded", e => {

		//CREATE SESSION
		devSeater.currentUser()
		.then(user => {
			Session.createSession(user);
		})
		.catch(err => console.error(err));

		//CHECKING
		checkNewMessages();
		checkNotifications();

		function checkNewMessages(){
			setTimeout(()=>{
				//Check new message number
				devSeater.newDialogNumber()
				.then(result => {
					ui.showNewDialogNumber(result["number"]);
				})
				.catch(err => console.error(err))
				.finally(() => {
					checkNewMessages();
				});
	
			}, 3000);
		}
		
		function checkNotifications(){
			setTimeout(()=>{
				//Check new notifications number
				devSeater.newNotificationNumber()
				.then(result => {
					ui.showNewNotificationNumber(result["number"]);
				})
				.catch(err => console.error(err))
				.finally(() => {
					checkNotifications();
				});
	
			}, 3000);
		}

	});

	searchInput.addEventListener('keydown', e => {
		query = e.target.value;
		
		if(query.length >= 2 && e.code != "Enter"){
			devSeater.generalSearch(query)
			.then(results => ui.showGeneralResults(results))
			.catch(err => console.error(err));
		}
		else{
			ui.hideGeneralSearchResults();
		}
	});

  
	searchForm.addEventListener('submit', e => {
		let url = searhResults.children[1].getAttribute("href");

		location.href = url;

		e.preventDefault();
	});

}