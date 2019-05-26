eventListeners();

function eventListeners(){

	document.addEventListener("submit", e => {
		if(e.target.classList.contains("comment-form")){
			let commentForm = e.target;
			let commentText = commentForm.querySelector("textarea").value;
			let post = commentForm.parentElement.parentElement;
			let ppid = post.getAttribute("ppid");
			
			ui.clearProjectPostCommentInput(ppid);

			devSeater.sendProjectPostComment(ppid, commentText)
			.then(response => {
				if(response["result"] == "success"){
					devSeater.userPostCommentNumber(ppid)
					.then(response => {
						ui.updateProjectPostCommentNumber(ppid, response["number"]);
						devSeater.userPostComments(ppid)
						.then(comments => {
							ui.clearProjectPostComments(ppid);
							ui.addProjectPostComments(ppid, comments, Session.getCurrentProject());
							ui.showProjectPostCommentBox(ppid);
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
				let ppid = parentElement.getAttribute("ppid");

				if(e.target.classList.contains("liked")){
					//Unlike the post
					devSeater.unlikeProjectPost(ppid)
					.then(response => {
						if(response["result"] == "success"){
							ui.unlikeProjectPost(ppid);

							devSeater.userPostLikeNumber(ppid)
							.then(response => {
								ui.updateProjectPostLikeNumber(ppid, response["number"]);
							})
							.catch(err => console.error(err));
						}
					})
					.catch(err => console.error(err));
				}
				else{
					//Like the post
					devSeater.likeProjectPost(ppid)
					.then(response => {
						if(response["result"] == "success"){
							ui.likeProjectPost(ppid);

							devSeater.userPostLikeNumber(ppid)
							.then(response => {
								ui.updateProjectPostLikeNumber(ppid, response["number"]);
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
				let ppid = parentElement.getAttribute("ppid");

				devSeater.userPostComments(ppid)
				.then(comments => {
					ui.clearProjectPostComments(ppid);
					ui.addProjectPostComments(ppid, comments, Session.getCurrentProject());
					ui.showProjectPostCommentBox(ppid);
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
			let ppid = post.getAttribute("ppid");

			let firstComment = commentsArea.firstElementChild;
			let firstUpcid = firstComment.getAttribute("upcid");

			if(confirm("Are you sure to delete this comment? This is permanent!")){

				devSeater.deleteProjectPostComment(upcid)
				.then(response => {
					if(response["ok"]){
						ui.removeProjectPostComment(upcid);
	
						devSeater.previousProjectPostComments(ppid, firstUpcid, 1)
						.then(comments => {
							ui.addProjectPostComments(ppid, comments, Session.getCurrentProject());
							
							devSeater.userPostCommentNumber()
							.then(response => {
								ui.updateProjectPostCommentNumber(ppid, response["number"]);
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
					devSeater.unlikeProjectPostComment(upcid)
					.then(response => {
						if(response["result"] == "success"){
							ui.unlikeProjectPostComment(upcid);
							
							devSeater.userPostCommentLikeNumber(upcid)
							.then(response => {
								ui.updateProjectPostCommentLikeNumber(upcid, response["number"]);
							})
							.catch(err => console.error(err));

						}
					})
					.catch(err => console.error(err));
				}
				else{
					devSeater.likeProjectPostComment(upcid)
					.then(response => {
						if(response["result"] == "success"){
							ui.likeProjectPostComment(upcid);

							devSeater.userPostCommentLikeNumber(upcid)
							.then(response => {
								ui.updateProjectPostCommentLikeNumber(upcid, response["number"]);
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
			let ppid = post.getAttribute("ppid");
			let upcid = e.target.parentElement.querySelector(".comments").firstElementChild.getAttribute("upcid");

			devSeater.previousProjectPostComments(ppid, upcid)
			.then(comments => {
				ui.addProjectPostComments(ppid, comments, Session.getCurrentProject());
			})
			.catch(err => console.error(err));
		}
			

		if(e.target.classList.contains("delete-post")){
			let post = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
			let ppid = post.getAttribute("ppid");
			
			if(confirm("Are you sure to delete this post? This is permanent!")){
				devSeater.deleteProjectPost(ppid)
				.then(response => {
					if(response["ok"]){
						ui.removeProjectPost(ppid);
					}
				})
				.catch(err => console.log(err));
			}
		}
		else if(e.target.classList.contains("edit-post")){
			let post = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
			let ppid = post.getAttribute("ppid");
			console.log(ppid);
		}
	});

}