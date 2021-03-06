//Selecting elements
const postTextArea = document.getElementById("post-textarea");
const postButton = document.getElementById("post-button");
const newFollowingPostNumberButton = document.getElementById("new-following-post-number");

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

		//CHECKING
		checkNewFollowingPosts();

		function checkNewFollowingPosts(){
			setTimeout(()=>{
				//Check new notifications number
				let theNewestPost = getTheNewestPost();
				if(theNewestPost == null){
					var theNewest_upid = 0;
				}
				else{
					var theNewest_upid = theNewestPost.getAttribute("upid");
				}

				devSeater.newFollowingPostNumber(theNewest_upid)
				.then(result => {
					ui.showNewFollowingPostNumber(result["number"]);
				})
				.catch(err => console.error(err))
				.finally(() => {
					checkNewFollowingPosts();
				});
	
			}, 4500);
		}
	});

	if(newFollowingPostNumberButton != null){
		newFollowingPostNumberButton.addEventListener("click", e => {
			let theNewestPost = getTheNewestPost();
			if(theNewestPost == null){
				var theNewest_upid = 0;
			}
			else{
				var theNewest_upid = theNewestPost.getAttribute("upid");
			}
			
			devSeater.newFollowingPosts(theNewest_upid)
			.then(posts => {

				//Render markdown
				posts = renderPosts(posts);

				ui.showNewFollowingPosts(posts, Session.getCurrentUser());
				PR.prettyPrint();	
			})
			.catch(err => console.error(err));
		});
	}
	
	if(postButton != null){
		postButton.addEventListener('click', e => {
			devSeater.sendUserPost(simplemde.value().trim())
			.then(response => {
				if (response["result"] == "success"){
					ui.showPostAlert("success");
					simplemde.value("");
				}
			})
		});
	}

	//When touched the bottom
	window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
			// Load previous following posts
			let lastPost = getTheLastPost();
			let upid = lastPost.getAttribute("upid");

			devSeater.previousFollowingPosts(upid)
			.then(posts => {
				//Render markdown
				posts.forEach(post => {
					post["post"] = markDownConverter.makeHtml(post["post"]);
				});

				ui.showPreviousFollowingPosts(posts, Session.getCurrentUser());
				PR.prettyPrint();
			})
			.catch(err => console.error(err));

    }
	};

}


