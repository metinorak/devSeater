//Selecting elements
const postTextArea = document.getElementById("post-textarea");
const postButton = document.getElementById("post-button");
const fullDescriptionInput = document.getElementsByName("full-description")[0];
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

				ui.showNewFollowingPosts(posts, Session.getCurrentUser());
			})
			.catch(err => console.error(err));
		});
	}
	
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
			})
			.catch(err => console.error(err));

    }
};

}

function getTheNewestPost(){
	return document.querySelector(".post");
}

function getTheLastPost(){
	let posts = document.querySelectorAll(".post");
	return posts[posts.length - 1];
}

