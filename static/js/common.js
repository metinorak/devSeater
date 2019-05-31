//Selecting elements
const memberOptions = document.getElementById("member-options");
const navbarLinks = document.getElementById("navbar-links");
const searchInput = document.getElementById("search-input");
const searhResults = document.getElementById("search-results");
const searchForm = document.getElementById("search-form");
const timeInfos = document.querySelectorAll(".time");

const ui = new UI();
const devSeater = new DevSeater();
const markDownConverter = new showdown.Converter({extensions: ['prettify']});

// Time info type changing
ui.changeTimeFormats(timeInfos);


eventListeners();

function eventListeners(){

  document.addEventListener("click", e => {
    
    if(e.target.classList.contains("follow-button")){
      let uid = e.target.parentElement.getAttribute("uid");

      if(e.target.classList.contains("followed")){
        //Unfollow the user
        devSeater.unFollow(uid)
        .then(response => {
          if(response["result"] == "success"){
            ui.unFollow(e.target);
          }
        })
        .catch(err => console.error(err));
      }
      else{
        //Follow the user
        devSeater.follow(uid)
        .then(response => {
          if(response["result"] == "success"){
            ui.follow(e.target);
          }
        })
        .catch(err => console.error(err));
      }

    }

  });

	document.addEventListener("DOMContentLoaded", e => {

		//RENDER MARKDOWN
		document.querySelectorAll(".post-body").forEach(post => {
			post.innerHTML = markDownConverter.makeHtml(post.textContent.trim());
		});

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

	document.addEventListener("click", e => {
		if (e.target != searhResults){
			ui.hideGeneralSearchResults();
		}
	});

}

function getTheNewestPost(){
	return document.querySelector(".post");
}

function getTheLastPost(){
	let posts = document.querySelectorAll(".post");
	return posts[posts.length - 1];
}

function renderPosts(posts){
	//Render markdown
	posts.forEach(post => {
		post["post"] = renderText(post["post"]);
	});

	return posts;
}

function renderText(text){
	return markDownConverter.makeHtml(text);
}
