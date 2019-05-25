class UI{
  constructor(){
    this.searchResults = document.getElementById("search-results");
    this.messagesLink = document.getElementById("messages-link");
    this.notificationsLink = document.getElementById("notifications-link");
    this.postButton = document.getElementById("post-button");
    this.addAnotherLinkButton = document.getElementById("add-another-link-button");
    this.newFollowingPostNumberButton = document.getElementById("new-following-post-number");
    this.theNewestPost = document.querySelector(".post");
    this.postTextarea = document.getElementById("post-textarea");

  }

  showGeneralResults(results){
    let desiredString = "";
    let userResultsString = "";
    let projectResultsString = "";

    if(results["userResults"].length > 0){
      results["userResults"].forEach(user => {
        userResultsString += (
          `<a href="/u/${user.username}" class="list-group-item list-group-item-action">${user.full_name}`+
          `<br><span class="text-muted">@${user.username}</span></a>`
          );  
      });
      desiredString += ("<h5>Users</h5>" + userResultsString);
    }

    if(results["projectResults"].length > 0){
      results["projectResults"].forEach(project => {
        projectResultsString += `<a href="/p/${project.project_name}" class="list-group-item list-group-item-action">${project.project_name}</a>`;  
      });

      desiredString += ( "<h5>Projects</h5>" + projectResultsString);
    }

    if(results["userResults"].length > 0 || results["projectResults"].length > 0){
      this.searchResults.innerHTML = desiredString;
      this.searchResults.style.display = "block";
    }


  }

  hideGeneralSearchResults(){
    this.searchResults.style.display = "none";
  }

  showNewDialogNumber(number){
    if(Number(number) > 0){
      this.messagesLink.lastElementChild.textContent = number;
      this.messagesLink.lastElementChild.style.display = "inline";
    }
    else if(this.messagesLink.lastElementChild.style.display == "inline"){
      this.messagesLink.lastElementChild.style.display == "none"
    }
    
  }

  showNewNotificationNumber(number){
    if(Number(number) > 0){
      this.notificationsLink.lastElementChild.textContent = number;
      this.notificationsLink.lastElementChild.style.display = "inline";
    }
    else if(this.notificationsLink.lastElementChild.style.display == "inline"){
      this.notificationsLink.lastElementChild.style.display == "none"
    }

  }

  showUserPostAlert(type){
    let alert = document.createElement("p");
    if(type == "success"){
      alert.setAttribute("style", "color: #89bda5; font-weight: bold; float:right;");
      alert.innerText = "The post was sent successfully!";
    }
    
    this.postButton.parentElement.appendChild(alert);

    setTimeout(()=>{
      this.postButton.parentElement.lastElementChild.remove();
    }, 3000);
  }

  addAnotherLinkInputToTheCreateProjectPage(){

    let newInput = document.createElement("div");
    newInput.setAttribute("class", "form-row");

    newInput.innerHTML = `
    <div class="col-md-8 mt-2">
    <input type="text" class="form-control" name="links[]" placeholder="http://">
    </div>
    <div class="col-md-4 mt-2">
      <input type="text" class="form-control" name="link-names[]" placeholder="link name">
    </div>
    `;

    this.addAnotherLinkButton.parentElement.previousElementSibling.appendChild(newInput);
    window.scrollTo(0,document.body.scrollHeight);
  }

  showNewFollowingPostNumber(number){
    if(Number(number) > 0){
      this.newFollowingPostNumberButton.style.display = "block";
      this.newFollowingPostNumberButton.textContent = `${number} new post(s)`;
    }
  }

  showNewFollowingPosts(posts, currentUser){
    posts.forEach((post) => {
      let postToAdd = document.createElement("div");
      postToAdd.setAttribute("class", "post");
      postToAdd.setAttribute("upid", post["upid"]);

      //Specify photo
      if (post["photo"] === null){
        var userPhoto = "/static/img/empty-profile.png";
      }
      else{
        var userPhoto = `/static/uploads/users/up/${post['photo']}`;
      }

      //Specify drop menu content
      if(post["uid"] == currentUser["uid"]){
        var menuContent = 
        `
        <li><a class="dropdown-item delete-post">Delete</a></li>
        <li><a class="dropdown-item edit-post">Edit</a></li>
        `;
      }
      else{
        var menuContent = ``;
      }

      if(post["isLiked"] == "1"){
        var likeButton = `<button class="btn btn-post mr-2 like-button liked">Like</button>`;
      }
      else{
        var likeButton = `<button class="btn btn-post mr-2 like-button">Like</button>`;
      }

      if(post["commentNumber"] > 0){
        var commentNumber = `<a href="#" class="comment-number">${post["commentNumber"]}</a>`;
      }
      else{
        var commentNumber = `<a href="#" class="comment-number"></a>`;
      } 


      if(post["likeNumber"] > 0){
        var likeNumber = `<a href="#" class="like-number">${post["likeNumber"]}</a>`;
      }
      else{
        var likeNumber = `<a href="#" class="like-number"></a>`;
      } 

      postToAdd.innerHTML = 
        `
          <div class="post-header mb-2">
          <a href="/u/${post['username']}">
            <span ><img width="55px" class="rounded-circle" src="${userPhoto}" alt=""></span>
          </a>    
          <span>
              <a href="/u/${post['username']}">
                  <h4>${post['full_name']}</h4>
                  <span style="font-size:13px" class="text-muted">@${post['username']}</span>
              </a>
              <p class="time">${this.timeSince(post["time"])} ago</p>
          </span>
          <span class="float-right">
              <div class="dropdown">
                  <button type="button" class="btn btn-basic" data-toggle="dropdown"><b>...</b></button>
                  <ul class="dropdown-menu">
                    ${menuContent}
                  </ul>
              </div>
          </span>
      </div>

      <div class="post-body mb-2">
      <?prettify?>
      <p>${post['post']}</p>
      </div>

      <div class="post-footer">
      <hr>
      <span class="row container post-footer-links mb-2">
          ${likeNumber}
          ${commentNumber}
      </span>
      ${likeButton}
      <button class="btn btn-post mr-2 comment-button">Comment</button>
      <button class="btn btn-post mr-2">Share</button>
      </div>

      <div style="display: none;" class="comment-box mt-2">
          <form class="row container comment-form">
              <textarea class="form-control col-sm-10" rows="1" placeholder="Add a comment..."></textarea>
              <input class="col-sm-2 btn btn-secondary container" type="submit" value="Send">
          </form>
          <button  class="btn btn-link load-comments">Load previous comments...</button>
          
          <div class="comments container">
              
          </div>

      </div>

        `;
        let theNewestPost = document.querySelector(".post");
        theNewestPost.insertAdjacentElement("beforebegin", postToAdd);
        
    });

    this.newFollowingPostNumberButton.style.display = "none";
  }

  showPreviousFollowingPosts(posts, currentUser){
    posts.forEach(post => {
      this.addPostToTheBottom(post, currentUser);
    });
  }

  showPreviousUserPosts(posts, currentUser){
    let contentArea = document.querySelector(".content-area");
    posts.forEach(post => {
      this.addPostToTheBottom(post, currentUser);
    });
  }

  showUserPosts(posts, currentUser){
    let contentArea = document.querySelector(".content-area");

    posts.forEach(post => {
      this.addPostToTheBottom(post, currentUser, contentArea);
    });
  }

  showUserSeaters(seaters){
    let contentArea = document.querySelector(".content-area");

    if(seaters.length == 0){
      contentArea.textContent = "This user has no seater.";
      return;
    }

    let innerContainer = document.createElement("div");
    innerContainer.className = "d-flex flex-wrap";
    contentArea.appendChild(innerContainer);

    seaters.forEach(seater => {
      this.addSeaterToTheBottom(seater, innerContainer);
    });
  }

  showUserSkills(skills){
    let contentArea = document.querySelector(".content-area");

    if(skills.length == 0){
      contentArea.textContent = "This user doesnt't have any seater.";
      return;
    }

    let innerContainer = document.createElement("div");
    innerContainer.className = "d-flex flex-wrap";
    contentArea.appendChild(innerContainer);

    skills.forEach(skill => {
      this.addSkillToTheBottom(skill, innerContainer);
    });
  }

  clearContentArea(){
    let contentArea = document.querySelector(".content-area");
    contentArea.innerHTML = "";
  }

  addSeaterToTheBottom(seater, container){
    if(seater["photo"] == null){
      seater["photo"] = "/static/img/empty-project.png";
    }
    else{
      seater["photo"] = "/static/uploads/projects/pp/" + seater["photo"];
    }

    let html = 
    `
    <div class="card seater m-2" sid="${seater["sid"]}" style="width: 18rem;">
      <img class="card-img-top" src="${seater["photo"]}" alt="Project Photo">
      <div class="card-body">
        <h3 class="card-title">${seater["title"]}</h3>
        <a href="/p/${seater["project_name"]}"><h4 class="card-title">${seater["project_name"]}</h4></a>
        <p class="card-text">${seater["short_description"].substr(0, 100)}</p>
        <a href="/p/${seater["project_name"]}/seaters/${seater["sid"]}" class="btn btn-primary">Browse</a>
      </div>
    </div>
    `;

    container.innerHTML += html;

  }

  addSkillToTheBottom(skill, container){
    let skillSpan = document.createElement("span");
    skillSpan.className = "skill";
    skillSpan.innerText = skill["name"];

    container.appendChild(skillSpan);
  }

  addPostToTheBottom(post, currentUser, container = null){
    let posts = document.querySelectorAll(".post");
    let lastPost = posts[posts.length - 1];

    let postToAdd = document.createElement("div");
    postToAdd.setAttribute("class", "post");
    postToAdd.setAttribute("upid", post["upid"]);

    //Specify photo
    if (post["photo"] === null){
      var userPhoto = "/static/img/empty-profile.png";
    }
    else{
      var userPhoto = `/static/uploads/users/up/${post['photo']}`;
    }

    //Specify drop menu content
    if(post["uid"] == currentUser["uid"]){
      var menuContent = 
      `
      <li><a class="dropdown-item delete-post">Delete</a></li>
      <li><a class="dropdown-item edit-post">Edit</a></li>
      `;
    }
    else{
      var menuContent = ``;
    }

    if(post["isLiked"] == "1"){
      var likeButton = `<button class="btn btn-post mr-2 like-button liked">Like</button>`;
    }
    else{
      var likeButton = `<button class="btn btn-post mr-2 like-button">Like</button>`;
    }

    if(post["commentNumber"] > 1){
      var commentNumber = `<a href="#" class="comment-number">${post["commentNumber"]} comments</a>`;
    }
    else if(post["commentNumber"] == 1){
      var commentNumber = `<a href="#" class="comment-number">1 comment</a>`;
    }
    else{
      var commentNumber = `<a href="#" class="comment-number"></a>`;
    } 


    if(post["likeNumber"] > 1){
      var likeNumber = `<a href="#" class="like-number mr-2">${post["likeNumber"]} </a>`;
    }
    else if(post["likeNumber"] == 1){
      var likeNumber = `<a href="#" class="like-number mr-2">1 like</a>`;
    }
    else{
      var likeNumber = `<a href="#" class="like-number"></a>`;
    } 



    //Render markdown

    postToAdd.innerHTML = 
      `
        <div class="post-header mb-2">
        <a href="/u/${post['username']}">
          <span ><img width="55px" class="rounded-circle" src="${userPhoto}" alt=""></span>
        </a>    
        <span>
            <a href="/u/${post['username']}">
                <h4>${post['full_name']}</h4>
                <span style="font-size:13px" class="text-muted">@${post['username']}</span>
            </a>
            <p class="time">${this.timeSince(post["time"])} ago</p>
        </span>
        <span class="float-right">
            <div class="dropdown">
                <button type="button" class="btn btn-basic" data-toggle="dropdown"><b>...</b></button>
                <ul class="dropdown-menu">
                  ${menuContent}
                </ul>
            </div>
        </span>
    </div>

    <div class="post-body mb-2">
    <?prettify?>
    <p>${post['post']}</p>
    </div>

    <div class="post-footer">
    <hr>
    <span class="row container post-footer-links mb-2">
        ${likeNumber}
        ${commentNumber}
    </span>
    ${likeButton}
    <button class="btn btn-post mr-2 comment-button">Comment</button>
    <button class="btn btn-post mr-2">Share</button>
    </div>

    <div style="display: none;" class="comment-box mt-2">
        <form class="row container comment-form">
            <textarea class="form-control col-sm-10" rows="1" placeholder="Add a comment..."></textarea>
            <input class="col-sm-2 btn btn-secondary container" type="submit" value="Send">
        </form>
        <button  class="btn btn-link load-comments">Load previous comments...</button>
        
        <div class="comments container">
            
        </div>

    </div>
      `;
      if(container == null){
        lastPost.insertAdjacentElement("afterend", postToAdd);
      }
      else{
        container.appendChild(postToAdd);
      }

  }  

  removeUserPost(upid){
    upid = upid.trim();
    let post = document.querySelector(`.post[upid="${upid}"]`);
    post.remove();
  }

  likeUserPost(upid){
    let post = document.querySelector(`.post[upid="${upid}"]`);
    let likeButton = post.querySelector(".like-button");
    likeButton.classList.add("liked");
    likeButton.textContent = "Liked";
  }

  unlikeUserPost(upid){
    let post = document.querySelector(`.post[upid="${upid}"]`);
    let likeButton = post.querySelector(".like-button");
    likeButton.classList.remove("liked");
    likeButton.textContent = "Like";
  }


  likeUserPostComment(upcid){
    let comment = document.querySelector(`.comment[upcid="${upcid}"]`);
    let commentLikeButton = comment.querySelector(".comment-like-button");
    commentLikeButton.classList.add("liked");
    commentLikeButton.textContent = "Liked";
  }

  unlikeUserPostComment(upcid){
    let comment = document.querySelector(`.comment[upcid="${upcid}"]`);
    let commentLikeButton = comment.querySelector(".comment-like-button");
    commentLikeButton.classList.remove("liked");
    commentLikeButton.textContent = "Like";
  }

  updateUserPostLikeNumber(upid, number){
    let post = document.querySelector(`.post[upid="${upid}"]`);
    let likeNumber = post.querySelector(".like-number");

    if(number > 1){
      likeNumber.textContent = `${number} likes`;
    }
    else if(number == 1){
      likeNumber.textContent = `${number} like`;
    }
    else{
      likeNumber.textContent = "";
    }
  }

  updateUserPostCommentNumber(upid, number){
    let post = document.querySelector(`.post[upid="${upid}"]`);
    let commentNumber = post.querySelector(".comment-number");
    
    if(number > 1){
      if(!commentNumber.classList.contains("ml-3")){
        commentNumber.classList.add("ml-3");
      }
      commentNumber.textContent = `${number} comments`;
    }
    else if(number == 1){
      if(!commentNumber.classList.contains("ml-3")){
        commentNumber.classList.add("ml-3");
      }
      commentNumber.textContent = `${number} comment`;
    }
    else{
      if(commentNumber.classList.contains("ml-3")){
        commentNumber.classList.remove("ml-3");
      }
      commentNumber.textContent = "";
    }
  }


  updateUserPostCommentLikeNumber(upcid, number){
    let comment = document.querySelector(`.comment[upcid="${upcid}"]`);
    let likeNumber = comment.querySelector(".like-number");

    if(number > 1){
      if(!likeNumber.classList.contains("mr-2")){
        likeNumber.classList.add("mr-2");
      }

      likeNumber.textContent = `(${number} likes)`;
    }
    else if(number == 1){
      if(!likeNumber.classList.contains("mr-2")){
        likeNumber.classList.add("mr-2");
      }

      likeNumber.textContent = `(1 like)`;
    }
    else{
      if(likeNumber.classList.contains("mr-2")){
        likeNumber.classList.remove("mr-2");
      }

      likeNumber.textContent = "";
    }
  }

  showUserPostCommentBox(upid){
    let post = document.querySelector(`.post[upid="${upid}"]`);
    let commentForm = post.querySelector(".comment-form");
    commentForm.focus();
    post.querySelector(".comment-box").style.display = "block";
  }

  closeUserPostCommentBox(upid){
    let post = document.querySelector(`.post[upid="${upid}"]`);
    post.querySelector(".comment-box").style.display = "none";
  }

  addUserPostComments(upid, comments, currentUser){
    let post = document.querySelector(`.post[upid="${upid}"]`);
    let commentsArea = post.querySelector(".comments");

    comments.forEach(comment => {

      if(comment["photo"] == null){
        comment["photo"] = "/static/img/empty-profile.png";
      }

      if(comment["isLiked"] == 1){
        var likeButton = `<button class="comment-like-button mr-2 liked">Liked</button>`;
      }
      else{
        var likeButton = `<button class="comment-like-button mr-2">Like</button>`;
      }

      if(comment["uid"] = currentUser["uid"]){
        var deleteButton = `<button class="comment-delete-button mr-2">Delete</button>`;
      }
      else{
        var deleteButton = "";
      }

      if(comment["likeNumber"] == 1){
        var likeNumber = `<span class="small mr-2 like-number">(1 like)</span>`;
      }
      else if(comment["likeNumber"] > 1){
        var likeNumber = `<span class="small mr-2 like-number">(${comment["likeNumber"]} likes)</span>`;
      }
      else{
        var likeNumber = `<span class="small like-number"></span>`;
      }

      let html = 
      `
      <div class="comment row mt-2" upcid = ${comment["upcid"]}>
        <a href="/u/${comment["username"]}" class="col-sm-1">
            <img width="30px" class="rounded-circle" src="${comment["photo"]}" alt="">
        </a>
        <div class="col-sm-2">
            <a href="/u/${comment["username"]}" class="row small">${comment["full_name"]}</a>
            <a href="/u/${comment["username"]}" class="row text-muted small">@${comment["username"]}</a>

        </div>
        <div class="col-sm-9">
          <span class="comment-text row">${comment["comment"]}</span>
          <span class="row">
            ${likeButton}
            ${deleteButton}
            ${likeNumber}
            <span class="time small text-muted text-italic">${this.timeSince(comment["time"])} ago</span>
          </span>
        </div>
      </div>
      `;

      commentsArea.innerHTML = (html + commentsArea.innerHTML);

    });
  }

  clearUserPostComments(upid){
    let post = document.querySelector(`.post[upid="${upid}"]`);
    let commentsArea = post.querySelector(".comments");
    
    commentsArea.textContent = "";
  }

  clearUserPostCommentInput(upid){
    let post = document.querySelector(`.post[upid="${upid}"]`);
    let commentForm = post.querySelector(".comment-form");
    commentForm.querySelector("textarea").value = "";

  }

  removeUserPostComment(upcid){
    let comment = document.querySelector(`.comment[upcid="${upcid}"]`);
    comment.remove();
  }

  changeTimeFormats(timeInfos){
    timeInfos.forEach(info => {
      info.textContent = this.timeSince(info.textContent) + " ago";
    });
  }


  timeSince(date) {
    date = new Date(date);

    var seconds = Math.floor((new Date() - date) / 1000);

    var interval = Math.floor(seconds / 31536000);

    if (interval > 1) {
      return interval + " years";
    }
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) {
      return interval + " months";
    }
    interval = Math.floor(seconds / 86400);
    if (interval > 1) {
      return interval + " days";
    }
    interval = (seconds / 3600);
    if (interval > 1) {
      return Math.floor(interval) + " hours";
    }
    interval = (seconds / 60);
    if (interval > 1) {
      return Math.floor(interval) + " minutes";
    }
    return Math.floor(seconds) + " seconds";
  }

  follow(followButton){
    followButton.textContent = "Followed";
    followButton.classList.add("followed");
  }

  unFollow(followButton){
    followButton.textContent = "Follow";
    followButton.classList.remove("followed");
  }

}