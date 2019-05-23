//Selecting elements
const memberOptions = document.getElementById("member-options");
const navbarLinks = document.getElementById("navbar-links");
const searchInput = document.getElementById("search-input");
const searhResults = document.getElementById("search-results");
const searchForm = document.getElementById("search-form");
const postTextArea = document.getElementById("post-textarea");
const postButton = document.getElementById("post-button");
const fullDescriptionInput = document.getElementsByName("full-description")[0];
const addAnotherLinkButton = document.getElementById("add-another-link-button");
const newFollowingPostNumberButton = document.getElementById("new-following-post-number");
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


//SIMPLEMDE textarea control

if(postTextArea != null){
	var simplemde = new SimpleMDE({
		element: postTextArea,
		showIcons: ["code"],
		hideIcons: ["side-by-side", "fullscreen"],
		spellChecker: false
	
	});
}

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
		checkNewFollowingPosts();

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

		function checkNewFollowingPosts(){
			setTimeout(()=>{
				//Check new notifications number
				let theNewestPost = getTheNewestPost();
				let theNewest_upid = theNewestPost.getAttribute("upid");

				devSeater.newFollowingPostNumber(theNewest_upid)
				.then(result => {
					ui.showNewFollowingPostNumber(result["number"]);
				})
				.catch(err => console.error(err))
				.finally(() => {
					checkNewFollowingPosts();
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

	document.addEventListener("submit", e => {
		if(e.target.classList.contains("comment-form")){
			let commentForm = e.target;
			let commentText = commentForm.querySelector("textarea").value;
			let post = commentForm.parentElement.parentElement;
			let upid = post.getAttribute("upid");
			
			ui.clearUserPostCommentInput(upid);

			devSeater.sendUserPostComment(upid, commentText)
			.then(response => {
				if(response["result"] == "success"){
					devSeater.userPostCommentNumber(upid)
					.then(response => {
						ui.updateUserPostCommentNumber(upid, response["number"]);
						devSeater.userPostComments(upid)
						.then(comments => {
							ui.clearUserPostComments(upid);
							ui.addUserPostComments(upid, comments, Session.getCurrentUser());
							ui.showUserPostCommentBox(upid);
						})
						.catch(err => console.error(err));
						
					})
					.catch(err => console.error(err));
					
				}
			})
			.catch(err => console.error(err));
		}

		e.preventDefault();
	});


	document.addEventListener('click', e => {

		if(e.target.classList.contains("like-button")){
			let parentElement = e.target.parentElement.parentElement;

			if(parentElement.classList.contains("post")){
				let upid = parentElement.getAttribute("upid");

				if(e.target.classList.contains("liked")){
					//Unlike the post
					devSeater.unlikeUserPost(upid)
					.then(response => {
						if(response["result"] == "success"){
							ui.unlikeUserPost(upid);

							devSeater.userPostLikeNumber(upid)
							.then(response => {
								ui.updateUserPostLikeNumber(upid, response["number"]);
							})
							.catch(err => console.error(err));
						}
					})
					.catch(err => console.error(err));
				}
				else{
					//Like the post
					devSeater.likeUserPost(upid)
					.then(response => {
						if(response["result"] == "success"){
							ui.likeUserPost(upid);

							devSeater.userPostLikeNumber(upid)
							.then(response => {
								console.log(response);
								ui.updateUserPostLikeNumber(upid, response["number"]);
							})
							.catch(err => console.error(err));
						}
					})
					.catch(err => console.error(err));
				}
			}
		}


		if(e.target.classList.contains("comment-button") || e.target.classList.contains("comment-number")){
			let parentElement;
			if(e.target.classList.contains("comment-number")){
				parentElement = e.target.parentElement.parentElement.parentElement;
			}
			else{
				parentElement = e.target.parentElement.parentElement;
			}

			if(parentElement.classList.contains("post")){
				let upid = parentElement.getAttribute("upid");

				devSeater.userPostComments(upid)
				.then(comments => {
					ui.clearUserPostComments(upid);
					ui.addUserPostComments(upid, comments, Session.getCurrentUser());
					ui.showUserPostCommentBox(upid);
				})
				.catch(err => console.error(err));

			}
			e.preventDefault();
		}

		if(e.target.classList.contains("comment-delete-button")){
			let comment = e.target.parentElement.parentElement.parentElement;
			let commentsArea = comment.parentElement;
			let upcid = comment.getAttribute("upcid");
			let post = comment.parentElement.parentElement.parentElement;
			let upid = post.getAttribute("upid");

			let firstComment = commentsArea.firstElementChild;
			let firstUpcid = firstComment.getAttribute("upcid");

			if(confirm("Are you sure to delete this comment? This is permanent!")){

				devSeater.deleteUserPostComment(upcid)
				.then(response => {
					if(response["ok"]){
						ui.removeUserPostComment(upcid);
	
						devSeater.previousUserPostComments(upid, firstUpcid, 1)
						.then(comments => {
							ui.addUserPostComments(upid, comments, Session.getCurrentUser());
							
							devSeater.userPostCommentNumber()
							.then(response => {
								ui.updateUserPostCommentNumber(upid, response["number"]);
							})
							.catch(err => console.error(err));
						})
						.catch(err => console.error(err));
	
					}
				})
				.catch(err => console.error(err));
	
			}
			
		}

		if(e.target.classList.contains("comment-like-button")){
			let parentElement = e.target.parentElement.parentElement.parentElement;

			if(parentElement.classList.contains("comment")){
				let upcid = parentElement.getAttribute("upcid");

				if(e.target.classList.contains("liked")){
					devSeater.unlikeUserPostComment(upcid)
					.then(response => {
						if(response["result"] == "success"){
							ui.unlikeUserPostComment(upcid);
							
							devSeater.userPostCommentLikeNumber(upcid)
							.then(response => {
								ui.updateUserPostCommentLikeNumber(upcid, response["number"]);
							})
							.catch(err => console.error(err));

						}
					})
					.catch(err => console.error(err));
				}
				else{
					devSeater.likeUserPostComment(upcid)
					.then(response => {
						if(response["result"] == "success"){
							ui.likeUserPostComment(upcid);

							devSeater.userPostCommentLikeNumber(upcid)
							.then(response => {
								ui.updateUserPostCommentLikeNumber(upcid, response["number"]);
							})
							.catch(err => console.error(err));

						}
					})
					.catch(err => console.error(err));
				}

			}
		}

		if(e.target.classList.contains("load-comments")){
			//Load previous comments
			let post = e.target.parentElement.parentElement;
			let upid = post.getAttribute("upid");
			let upcid = e.target.parentElement.querySelector(".comments").firstElementChild.getAttribute("upcid");

			devSeater.previousUserPostComments(upid, upcid)
			.then(comments => {
				ui.addUserPostComments(upid, comments, Session.getCurrentUser());
			})
			.catch(err => console.error(err));
		}
			

		if (e.target != searhResults){
			ui.hideGeneralSearchResults();
		}

		if(e.target.classList.contains("delete-post")){
			let post = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
			let upid = post.getAttribute("upid");
			
			if(confirm("Are you sure to delete this post? This is permanent!")){
				devSeater.deleteUserPost(upid)
				.then(response => {
					if(response["ok"]){
						ui.removeUserPost(upid);
					}
				})
				.catch(err => console.log(err));
			}
		}
		else if(e.target.classList.contains("edit-post")){
			let post = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
			let upid = post.getAttribute("upid");
			console.log(upid);
		}
	});

	if(newFollowingPostNumberButton != null){
		newFollowingPostNumberButton.addEventListener("click", e => {
			let theNewestPost = getTheNewestPost();
			let theNewest_upid = theNewestPost.getAttribute("upid");
			devSeater.newFollowingPosts(theNewest_upid)
			.then(posts => {

				//Render markdown
				posts.forEach(post => {
					post["post"] = markDownConverter.makeHtml(post["post"]);
				});

				let currentUser = Session.getCurrentUser();
				ui.showNewFollowingPosts(posts, currentUser);
			})
			.catch(err => console.error(err));
		});
	}
	
	
	searchForm.addEventListener('submit', e => {
		let url = searhResults.children[1].getAttribute("href");

		location.href = url;

		e.preventDefault();
	});

	if(postButton != null){
		postButton.addEventListener('click', e => {
			devSeater.sendUserPost(simplemde.value())
			.then(response => {
				if (response["result"] == "success"){
					ui.showUserPostAlert("success");
					simplemde.value("");
				}
			})
		});
	}

	if(addAnotherLinkButton != null){
		addAnotherLinkButton.addEventListener("click", e => {
			ui.addAnotherLinkInputToTheCreateProjectPage();
		});
	}

}

function getTheNewestPost(){
	return document.querySelector(".post");
}

