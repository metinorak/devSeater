class UI{
  constructor(){
    this.searchResults = document.getElementById("search-results");
    this.messagesLink = document.getElementById("messages-link");
    this.notificationsLink = document.getElementById("notifications-link");
    this.postButton = document.getElementById("post-button");
    this.addAnotherLinkButton = document.getElementById("add-another-link-button");
    this.newFollowingPostNumberButton = document.getElementById("new-following-post-number");
    this.postTextarea = document.getElementById("post-textarea");
    this.contentArea = document.querySelector(".content-area");
    this.navbar = document.querySelector("navbar");
    this.generalModal = document.querySelector("#general-modal");
    this.messageModal = document.querySelector("#message-modal");
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

  hideGeneralModal(){
    $("#general-modal").modal("hide");
  }

  showNewDialogNumber(number){
    if(Number(number) == 0){
      this.messagesLink.lastElementChild.style.display = "none";
    }
    else{
      this.messagesLink.lastElementChild.textContent = number;
      this.messagesLink.lastElementChild.style.display = "inline";
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

  showPostAlert(type){
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

  addAnotherLinkInput(container, url="", name=""){
    let newInput = document.createElement("div");
    newInput.setAttribute("class", "form-row");

    newInput.innerHTML = `
    <div class="col-md-8 mt-2">
    <input type="text" class="form-control" name="links[]" placeholder="http://" value="${url}">
    </div>
    <div class="col-md-4 mt-2">
      <input type="text" class="form-control" name="link-names[]" placeholder="link name" value="${name}">
    </div>
    `;

    container.appendChild(newInput);
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
        if(theNewestPost != null)
          theNewestPost.insertAdjacentElement("beforebegin", postToAdd);
        else{
          this.newFollowingPostNumberButton.insertAdjacentElement("afterend", postToAdd);
        }
        
    });

    this.newFollowingPostNumberButton.style.display = "none";
  }

  showPreviousFollowingPosts(posts, currentUser){
    posts.forEach(post => {
      this.addPostToTheBottom(post, currentUser);
    });
  }

  showPreviousPosts(posts, currentUser){
    posts.forEach(post => {
      this.addPostToTheBottom(post, currentUser);
    });
  }

  showPosts(posts, currentUser){
    

    posts.forEach(post => {
      this.addPostToTheBottom(post, currentUser, this.contentArea);
    });
  }

  showSeaters(seaters){
    if(seaters.length == 0){
      this.contentArea.textContent = "This user has no seater.";
      return;
    }

    let innerContainer = document.createElement("div");
    innerContainer.className = "d-flex flex-wrap";
    this.contentArea.appendChild(innerContainer);

    seaters.forEach(seater => {
      this.appendSeater(seater, innerContainer);
    });
  }

  showUserSkills(skills){
    if(skills.length == 0){
      this.contentArea.textContent = "This user has no skills.";
      return;
    }

    let innerContainer = document.createElement("div");
    innerContainer.className = "d-flex flex-wrap";
    this.contentArea.appendChild(innerContainer);

    skills.forEach(skill => {
      this.addSkillToTheBottom(skill, innerContainer);
    });
  }

  clearContentArea(){
    this.contentArea.innerHTML = "";
  }

  appendSeater(seater, container){
    if(seater["photo"] == null){
      seater["photo"] = "/static/img/empty-project.png";
    }
    else{
      seater["photo"] = "/static/uploads/projects/pp/" + seater["photo"];
    }

    if(seater["username"] == undefined){
      var usernameCode = "";
    }
    else{
      var usernameCode = `<p class="card-text"><a href="/u/${seater["username"]}"><b>@${seater["username"]}</b></a></p>`;
    }

    if(seater["aspirationNumber"] == undefined || seater["aspirationNumber"] == 0){
      var aspirationNumber = "";
    }
    else{
      var aspirationNumber = `<p class="card-text">${seater["aspirationNumber"]} aspiration(s)</p>`;
    }

    let html = 
    `
    <div class="card seater m-2" sid="${seater["sid"]}" style="width: 18rem;">
      <img class="card-img-top" src="${seater["photo"]}" alt="Project Photo">
      <div class="card-body">
        <h3 class="card-title">${seater["title"]}</h3>
        <a href="/p/${seater["project_name"]}"><h4 class="card-title">${seater["project_name"]}</h4></a>
        <p class="card-text">${seater["short_description"].substr(0, 100)}</p>
        ${usernameCode}
        ${aspirationNumber}
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
    if(post["upid"] != undefined){
      postToAdd.setAttribute("upid", post["upid"]);
    }
    else if(post["ppid"] != undefined){
      postToAdd.setAttribute("ppid", post["ppid"]);
    }

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
      var likeNumber = `<a href="#" class="like-number mr-2">${post["likeNumber"]} likes</a>`;
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
      likeNumber.classList.add("mr-2");
    }
    else if(number == 1){
      likeNumber.textContent = `${number} like`;
      likeNumber.classList.add("mr-2");
    }
    else{
      likeNumber.textContent = "";
      likeNumber.classList.remove("mr-2");
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
      else{
        comment["photo"] = "/static/uploads/users/up/" + comment["photo"];
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
          <p class="comment-text">${comment["comment"]}</p>
          <span >
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


  //PROJECT POSTS


  removeProjectPost(ppid){
    ppid = ppid.trim();
    let post = document.querySelector(`.post[ppid="${ppid}"]`);
    post.remove();
  }

  likeProjectPost(ppid){
    let post = document.querySelector(`.post[ppid="${ppid}"]`);
    let likeButton = post.querySelector(".like-button");
    likeButton.classList.add("liked");
    likeButton.textContent = "Liked";
  }

  unlikeProjectPost(ppid){
    let post = document.querySelector(`.post[ppid="${ppid}"]`);
    let likeButton = post.querySelector(".like-button");
    likeButton.classList.remove("liked");
    likeButton.textContent = "Like";
  }


  likeProjectPostComment(ppcid){
    let comment = document.querySelector(`.comment[ppcid="${ppcid}"]`);
    let commentLikeButton = comment.querySelector(".comment-like-button");
    commentLikeButton.classList.add("liked");
    commentLikeButton.textContent = "Liked";
  }

  unlikeProjectPostComment(ppcid){
    let comment = document.querySelector(`.comment[ppcid="${ppcid}"]`);
    let commentLikeButton = comment.querySelector(".comment-like-button");
    commentLikeButton.classList.remove("liked");
    commentLikeButton.textContent = "Like";
  }

  updateProjectPostLikeNumber(ppid, number){
    let post = document.querySelector(`.post[ppid="${ppid}"]`);
    let likeNumber = post.querySelector(".like-number");

    if(number > 1){
      likeNumber.textContent = `${number} likes`;
      likeNumber.classList.add("mr-2");
    }
    else if(number == 1){
      likeNumber.textContent = `${number} like`;
      likeNumber.classList.add("mr-2");
    }
    else{
      likeNumber.textContent = "";
      likeNumber.classList.remove("mr-2");
    }
  }

  updateProjectPostCommentNumber(ppid, number){
    let post = document.querySelector(`.post[ppid="${ppid}"]`);
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


  updateProjectPostCommentLikeNumber(ppcid, number){
    let comment = document.querySelector(`.comment[upcid="${ppcid}"]`);
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

  showProjectPostCommentBox(ppid){
    let post = document.querySelector(`.post[ppid="${ppid}"]`);
    let commentForm = post.querySelector(".comment-form");
    commentForm.focus();
    post.querySelector(".comment-box").style.display = "block";
  }

  closeProjectPostCommentBox(ppid){
    let post = document.querySelector(`.post[ppid="${ppid}"]`);
    post.querySelector(".comment-box").style.display = "none";
  }

  addProjectPostComments(ppid, comments, currentUser){
    let post = document.querySelector(`.post[ppid="${ppid}"]`);
    let commentsArea = post.querySelector(".comments");

    comments.forEach(comment => {

      if(comment["photo"] == null){
        comment["photo"] = "/static/img/empty-profile.png";
      }
      else{
        comment["photo"] = "/static/uploads/users/up/" + comment["photo"];
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
      <div class="comment row mt-2" ppcid = ${comment["ppcid"]}>
        <a href="/u/${comment["username"]}" class="col-sm-1">
            <img width="30px" class="rounded-circle" src="${comment["photo"]}" alt="">
        </a>
        <div class="col-sm-2">
            <a href="/u/${comment["username"]}" class="row small">${comment["full_name"]}</a>
            <a href="/u/${comment["username"]}" class="row text-muted small">@${comment["username"]}</a>

        </div>
        <div class="col-sm-9">
          <p class="comment-text">${comment["comment"]}</p>
          <span >
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

  clearProjectPostComments(ppid){
    let post = document.querySelector(`.post[ppid="${ppid}"]`);
    let commentsArea = post.querySelector(".comments");
    
    commentsArea.textContent = "";
  }

  clearProjectPostCommentInput(ppid){
    let post = document.querySelector(`.post[ppid="${ppid}"]`);
    let commentForm = post.querySelector(".comment-form");
    commentForm.querySelector("textarea").value = "";

  }

  removeProjectPostComment(ppcid){
    let comment = document.querySelector(`.comment[ppcid="${ppcid}"]`);
    comment.remove();
  }

  showProjectMembers(members, currentUser){
    

    if(members.length == 0){
      this.contentArea.textContent = "This user has no seater.";
      return;
    }

    let container = document.createElement("div");
    container.className = "d-flex flex-wrap";
    this.contentArea.appendChild(container);

    members.forEach(member => {
      this.appendMember(member, currentUser, container);
    });

    this.contentArea.append(container);
  }

  appendMember(member, currentUser, container){
    let memberCard = document.createElement("div");
    memberCard.className = "member-card";
    memberCard.setAttribute("uid", member["uid"]);

    if(member["photo"] == null){
      var imgAddress = "/static/img/empty-profile.png";
    }
    else{
      var imgAddress = `/static/uploads/users/up/${member["photo"]}`;
    }

    if(currentUser["uid"] == member["uid"]){
      var followButton = "";
    }
    else if(member["isFollowed"]){
      var followButton = `<button class="btn btn-light follow-button following">Following</button>`;
    }
    else{
      var followButton = `<button class="btn btn-light follow-button">Follow</button>`;
    }
    
    if(member["bio"] == null){
      member["bio"] = "";
    }
    
    let html = 
    `
      <a href="/u/${member["username"]}">
        <img class="profile-img" src="${imgAddress}" alt=""><br>
        <h2>${member["full_name"]}</h2>
        <span class="text-muted">@${member["username"]}</span><br>
      </a>
      <span>
        ${member["bio"]}
      </span><br>
      ${followButton}
    `;

    memberCard.innerHTML = html;
    container.appendChild(memberCard);

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
    followButton.textContent = "Following";
    followButton.classList.add("following");
  }

  unFollow(followButton){
    followButton.textContent = "Follow";
    followButton.classList.remove("following");
  }

  showPostTextAreaCard(){
    let card = document.querySelector(".post-textarea-card");
    card.style.display = "block";
  }

  hidePostTextAreaCard(){
    let card = document.querySelector(".post-textarea-card");
    card.style.display = "none";
  }


  showEmptySeaters(seaters, isProjectAdmin){
    if(!isProjectAdmin){
      var newSeaterButtonStyle = "display:none;";
    }
    else{
      var newSeaterButtonStyle = "display:inline;"; 
    }

    let tabsHtml = 
    ` <a href="#" id="create-a-new-seater" style="${newSeaterButtonStyle}" class="btn btn-secondary float-right">New Seater</a>
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a id="empty-seaters" class="nav-link active" href="#">Empty Seaters</a>
        </li>
        <li class="nav-item">
          <a id="filled-seaters" class="nav-link" href="#">Filled Seaters</a>
        </li>
      </ul>
    `;
    let tabsElement = document.createElement("div");
    tabsElement.innerHTML = tabsHtml;
    this.contentArea.appendChild(tabsElement);

    if(seaters.length == 0){
      let messageText = document.createElement("p");
      messageText.textContent = "This project has no empty seaters.";
      messageText.className = "mt-3";
      this.contentArea.appendChild(messageText);
      return;
    }

    let innerContainer = document.createElement("div");
    innerContainer.className = "d-flex flex-wrap";

    this.contentArea.appendChild(innerContainer);

    seaters.forEach(seater => {
      this.appendSeater(seater, innerContainer);
    });
  }

  showFilledSeaters(seaters, isProjectAdmin){
    if(!isProjectAdmin){
      var newSeaterButtonStyle = "display:none;";
    }
    else{
      var newSeaterButtonStyle = "display:inline;"; 
    }

    
    let tabsHtml = 
    ` <a href="#" id="create-a-new-seater" style="${newSeaterButtonStyle}" class="btn btn-secondary float-right">New Seater</a>
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a id="empty-seaters" class="nav-link" href="#">Empty Seaters</a>
        </li>
        <li class="nav-item">
          <a id="filled-seaters" class="nav-link active" href="#">Filled Seaters</a>
        </li>
      </ul>
    `;
    let tabsElement = document.createElement("div");
    tabsElement.innerHTML = tabsHtml;
    this.contentArea.appendChild(tabsElement);

    if(seaters.length == 0){
      let messageText = document.createElement("p");
      messageText.textContent = "This project has no filled seaters.";
      messageText.className = "mt-3";
      this.contentArea.appendChild(messageText);
      return;
    }
    
    let innerContainer = document.createElement("div");
    innerContainer.className = "d-flex flex-wrap";
    this.contentArea.appendChild(innerContainer);
    seaters.forEach(seater => {
      this.appendSeater(seater, innerContainer);
    });
  }

  showAboutText(text){
    

    if(text.trim().length == 0){
      text = "This project has no full description.";
    }

    this.contentArea.innerHTML = 
    `
    <div class="card border-dark mb-3">
      <div class="card-header">About The Project</div>
      <div class="card-body text-dark">
        <p class="card-text">${text.trim()}</p>
      </div>
    </div>
    `;
  }
  
  showUserProfileSettings(currentUser, links, skills){
  
    let linkList = document.createElement("ul");
    linkList.className = "list-group";
    links.forEach(l => {
      let element = document.createElement("li");
      element.setAttribute("ulid", l["ulid"]);
      element.className = "list-group-item";
      element.innerHTML = 
      `<a href="${l["link"]}">${l["name"]}</a>
       <a href="#" id="delete-user-link" class="btn btn-danger float-right">Delete</a>
       `;

      linkList.appendChild(element);
    });

    let skillList = document.createElement("ul");
    skillList.className = "list-group";
    skills.forEach(s => {
      let element = document.createElement("li");
      element.className = "list-group-item";
      element.setAttribute("skid", s["skid"]);
      element.innerHTML = 
      `<span>${s["name"]}</span>
       <a href="#" class="btn btn-danger float-right delete-user-skill">Delete</a>`;

      skillList.appendChild(element);
    });

    let card = 
    `
    <div class="card">
      <h5 class="card-header">Profile Settings</h5>
      <div class="card-body">
        <ul class="nav nav-tabs" id="user-setting-tabs" role="tablist">
          <li class="nav-item">
            <a class="nav-link active" id="user-tab" data-toggle="tab" href="#user-tab-content" role="tab" aria-controls="home" aria-selected="true">User</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" id="links-tab" data-toggle="tab" href="#links-tab-content" role="tab" aria-controls="profile" aria-selected="false">Links</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" id="skills-tab" data-toggle="tab" href="#skills-tab-content" role="tab" aria-controls="contact" aria-selected="false">Skills</a>
          </li>
        </ul>
        <div class="tab-content mt-2">
          <div class="tab-pane fade show active" id="user-tab-content" role="tabpanel" aria-labelledby="user-tab">
            <form>
              <div class="form-group">
                <label>Profile Photo (1:1 ratio)</label>
                <input type="file" accept="image" class="form-control" id="profile-photo" >
              </div>
            </form>
            <div class="form-group">
              <label>Full Name</label>
              <input type="text" class="form-control" id="user-full-name" placeholder="Full Name" value="${currentUser["full_name"]}">
            </div>

            <div class="form-group">
              <label>Bio (max 100 chars)</label>
              <textarea class="form-control" id="user-bio" rows="3" maxlength="100">${currentUser["bio"]}</textarea>
              <span class="char-number"></span>
            </div>

          </div>
          <div class="tab-pane fade" id="links-tab-content" role="tabpanel" aria-labelledby="links-tab">
          <div>${linkList.outerHTML}</div>
          <a href="#" id="add-new-link" class="btn btn-primary mt-2">Add new link</a>
          </div>
          <div class="tab-pane fade" id="skills-tab-content" role="tabpanel" aria-labelledby="skills-tab">
          <div>${skillList.outerHTML}</div>
          <a href="#" id="add-new-skill" class="btn btn-primary mt-2">Add new skill</a>
          </div>
        </div>

      </div>
    </div>
    `;

    this.contentArea.innerHTML = card;

    document.querySelector("#user-bio").addEventListener("input", e => {
      document.querySelector(".char-number").textContent = `char number: ${e.target.value.length}`;
    });
  }

  showMessageAfterElement(element, message, type = "success"){
    let messageElement = document.createElement("div");
    messageElement.className = "mt-3 user-msg";
    if(type == "info"){
      messageElement.style.color = "gray";
    }
    else if(type == "success"){
      messageElement.style.color = "lightgreen";
    }
    else if(type == "fail"){
      messageElement.style.color = "red";
    }
    messageElement.textContent = message;

    if(element.nextElementSibling != null && element.nextElementSibling.classList.contains("user-msg")){
      element.nextElementSibling.remove();
    }
    if(message != ""){
      element.insertAdjacentElement("afterend", messageElement);
    }
  }

  showAlert(element, message, type, position){
    let alert = document.createElement("div");
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    if(position == "beforebegin" && element.previousElementSibling != null && element.previousElementSibling.classList.contains("alert")){
      element.previousElementSibling.remove();
    }
    else if(position == "afterend" && element.nextElementSibling != null && element.nextElementSibling.classList.contains("alert")){
      element.nextElementSibling.remove();
    }
    else if(position == "afterbegin" && element.firtElementChild != null && element.firtElementChild.classList.contains("alert")){
      element.firtElementChild.remove();
    }
    else if(position == "beforeend" && element.lastElementChild != null && element.lastElementChild.classList.contains("alert")){
      element.lastElementChild.remove();
    }
    
    element.insertAdjacentElement(position, alert);
  }
  
  async getNewLinkFromUser(){
    return new Promise((resolve, reject) => {
      //Set General Modal
      let modalBody = document.createElement("div");
      let urlInput = document.createElement("input");
      urlInput.className = "form-control";
      urlInput.setAttribute("id", "url-input");
      urlInput.setAttribute("type", "text");
      urlInput.setAttribute("placeholder", "http://");

      let nameInput = document.createElement("input");
      nameInput.className = "form-control mt-2";
      nameInput.setAttribute("id", "name-input");
      nameInput.setAttribute("type", "text");
      nameInput.setAttribute("placeholder", "link name: (ex: Blog, Github, Twitter)");

      modalBody.appendChild(urlInput);
      modalBody.appendChild(nameInput);

      this.setModal(this.generalModal, "Add New Link", modalBody);

      let saveButton = this.generalModal.querySelector("#save-general-modal-changes");
      
      //Retrieve inputs
      saveButton.addEventListener("click", e => {
        let link = this.generalModal.querySelector("#url-input").value;
        let name = this.generalModal.querySelector("#name-input").value;
        $("#general-modal").modal("hide");
        resolve({link: link, name: name});
      });

      $("#general-modal").modal("show");

    });
  }

  async getNewSkillFromUser(){
    return new Promise((resolve, reject) => {
      //Set General Modal
      let modalBody = document.createElement("div");
      let skillInput = document.createElement("input");
      skillInput.className = "form-control";
      skillInput.setAttribute("id", "skill-input");
      skillInput.setAttribute("type", "text");
      skillInput.setAttribute("placeholder", "ex: Java, C++, OOP, Machine Learning");

      modalBody.appendChild(skillInput);

      this.setModal(this.generalModal, "Add New Skill", modalBody);

      let saveButton = this.generalModal.querySelector("#save-general-modal-changes");
      
      //Retrieve inputs
      saveButton.addEventListener("click", e => {
        let skill = this.generalModal.querySelector("#skill-input").value;
        $("#general-modal").modal("hide");
        resolve(skill);
      });

      $("#general-modal").modal("show");

    });
  }

  async getSeaterFromUser(seater=null){
    return new Promise((resolve, reject) => {
      //Seater edit
      let titleText = "";
      let shortDescriptionText = "";
      let fullDescriptionText = "";
      let skillsText = "";
      if(seater != null){
        titleText = seater["title"];
        shortDescriptionText = seater["short_description"];
        fullDescriptionText = seater["full_description"];
        seater["skills"].forEach((index, skill) => {
          if(index != (seater["skills"].length -1))
            skillsText += (skill["name"] + ",");
          else
          skillsText += (skill["name"] + ",");
        });
      }

      //Set General Modal
      let modalBody = document.createElement("div");
      let html = 
      `
      <form>
        <div class="form-group">
          <label for="title-input">Title</label>
          <input type="text" class="form-control" id="title-input" placeholder="ex: Java Developer" value="${titleText}">
        </div>
        <div class="form-group">
          <label for="short-description-input">Short Description (max 100 chars)</label>
          <input type="text" class="form-control" id="short-description-input" maxlength="100" value = "${shortDescriptionText}">
        </div>
        <div class="form-group">
          <label for="long-description-input">Full Description (markdown)</label>
          <textarea class="form-control" id="full-description-input"></textarea>
        </div>
        <div class="form-group">
          <label for="skills-input">Skills</label>
          <input type="text" class="form-control" id="skills-input" placeholder="separate the skills with commas." value="${skillsText}">
        </div>
        
      </form>
      `;
      modalBody.innerHTML = html;

      this.setModal(this.generalModal, "Add New Seater", modalBody);

      let simplemde = new SimpleMDE({
        element: this.generalModal.querySelector("#full-description-input"),
        showIcons: ["code"],
        hideIcons: ["side-by-side", "fullscreen"],
        spellChecker: false,
        initialValue: fullDescriptionText
      });

      let saveButton = this.generalModal.querySelector("#save-general-modal-changes");
      
      //Retrieve inputs
      saveButton.addEventListener("click", e => {
        let title = this.generalModal.querySelector("#title-input").value;
        let shortDescription = this.generalModal.querySelector("#short-description-input").value;
        let fullDescription = simplemde.value();
        let skills = this.generalModal.querySelector("#skills-input").value.trim().split(",");
        $("#general-modal").modal("hide");
        resolve({
          title: title,
          short_description: shortDescription,
          full_description: fullDescription,
          skills: skills
        });
      });

      $("#general-modal").modal("show");

    });
  }
  

  addLinkListItem(link, container){
    let element = document.createElement("li");
    if(link["ulid"] != undefined){
      element.setAttribute("ulid", link["ulid"]);
      element.innerHTML = 
      `<a href="${link["link"]}">${link["name"]}</a>
       <a href="#" id="delete-user-link" class="btn btn-danger float-right">Delete</a>
       `;
    }
    else{
      element.innerHTML = 
      `<a href="${link["link"]}">${link["name"]}</a>
       <a href="#" id="delete-project-link" class="btn btn-danger float-right">Delete</a>
       `;
      element.setAttribute("plid", link["plid"]);
    }
    element.className = "list-group-item";

    container.appendChild(element);
  }

  addSkillListItem(skill, container){
    let element = document.createElement("li");
    element.className = "list-group-item";
    element.setAttribute("skid", skill["skid"]);
    element.innerHTML = 
    `<span>${skill["name"]}</span>
     <a href="#" class="btn btn-danger float-right delete-user-skill">Delete</a>`;

    container.appendChild(element);
  }  
  
  showProjectPageSettings(project, links, mdeCallBack){
    let linkList = document.createElement("ul");
    linkList.className = "list-group";
    links.forEach(l => {
      let element = document.createElement("li");
      element.setAttribute("plid", l["plid"]);
      element.className = "list-group-item";
      element.innerHTML = 
      `<a href="${l["link"]}">${l["name"]}</a>
       <a href="#" class="btn btn-danger float-right" id="delete-project-link">Delete</a>
       `;

      linkList.appendChild(element);
    });

    let card = 
    `
    <div class="card">
      <h5 class="card-header">Project Settings</h5>
      <div class="card-body">
        <ul class="nav nav-tabs" id="project-setting-tabs" role="tablist">
          <li class="nav-item">
            <a class="nav-link active" id="project-tab" data-toggle="tab" href="#project-tab-content" role="tab" aria-controls="home" aria-selected="true">Project</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" id="links-tab" data-toggle="tab" href="#links-tab-content" role="tab" aria-controls="profile" aria-selected="false">Links</a>
          </li>
        </ul>
        <div class="tab-content mt-2">
          <div class="tab-pane fade show active" id="project-tab-content" role="tabpanel" aria-labelledby="project-tab">
            <form>
              <div class="form-group">
                <label>Project Photo (16:9 ratio)</label>
                <input type="file" accept="image" class="form-control" id="project-photo" >
              </div>
            </form>
            <div class="form-group">
              <label>Project Name</label>
              <input type="text" class="form-control" id="project-name" placeholder="Project Name" value="${project["project_name"]}">
            </div>

            <div class="form-group">
              <label>Short Description (max 100 chars)</label>
              <textarea class="form-control" id="project-short-description" rows="3" maxlength="100">${project["short_description"]}</textarea>
              <span class="char-number"></span>
            </div>

            <div class="form-group">
              <label>Full Description (markdown)</label>
              <textarea class="form-control" id="project-full-description">${project["full_description"]}</textarea>
              <span class="char-number"></span>
            </div>
          </div>
          <div class="tab-pane fade" id="links-tab-content" role="tabpanel" aria-labelledby="links-tab">
          <div>${linkList.outerHTML}</div>
          <a href="#" id="add-new-link" class="btn btn-primary mt-2">Add new link</a>
          </div>
        </div>
      </div>
    </div>
    `;

    this.contentArea.innerHTML = card;

    var simplemde = new SimpleMDE({
      element: this.contentArea.querySelector("#project-full-description"),
      showIcons: ["code"],
      hideIcons: ["side-by-side", "fullscreen"],
      spellChecker: false
    
    });

    mdeCallBack(simplemde);

    document.querySelector("#project-short-description").addEventListener("input", e => {
      document.querySelector(".char-number").textContent = `char number: ${e.target.value.length}`;
    });
  }

  showSeaterAspirationsList(aspirations){
    let modalBody = document.createElement("div");
    if(aspirations.length == 0){
      modalBody.textContent = "This seater has no aspirations.";
    }
    else{
      modalBody.className = "list-group";
      aspirations.forEach(aspiration => {
        let element = document.createElement("li");
        element.className = "list-group-item";
        element.setAttribute("uid", aspiration["uid"]);
        element.setAttribute("sid", aspiration["sid"]);
  
        if(aspiration["photo"] == null){
          aspiration["photo"] = "/static/img/empty-profile.png";
        }
        else{
          aspiration["photo"] = "/static/uploads/users/up/" + aspiration["photo"];
        }
  
        element.innerHTML =
        `
        <span class="row">
          <span class="col-sm-6">
            <a href="/u/${aspiration["username"]}">
              <span>${aspiration["full_name"]}</span><br>
              <span style="font-size:13px" class="text-muted">@${aspiration["username"]}</span>
            </a>
          </span>
          <span class="col-sm-3"><button id="assign-user-button" class="btn btn-primary">Assign</button></span>
          <span class="col-sm-3"><button id="reject-user-button" class="btn btn-danger">Reject</button></span>
        </span>
        `;
        modalBody.appendChild(element);
      });  
    }

    this.setModal(this.generalModal, "Aspirations", modalBody, true);
    $("#general-modal").modal("show");
  }

  showDialogList(dialogList){
    this.closeAllModals();

    let modalBody = document.createElement("div");
    if(dialogList.length == 0){
      modalBody.textContent = "You don't have any message :(";
    }
    else{
      modalBody.className = "list-group";
      dialogList.forEach(dialog => {
        let element = document.createElement("li");
        element.className = 
        `list-group-item ${dialog["isRead"] == 0 ? 'bg-new-message' : ''}`;
        element.setAttribute("uid", dialog["uid"]);
  
        if(dialog["photo"] == null){
          dialog["photo"] = "/static/img/empty-profile.png";
        }
        else{
          dialog["photo"] = "/static/uploads/users/up/" + dialog["photo"];
        }
  
        element.innerHTML =
        `
        <span class="row">
          <span class="col-sm-9">
            <a href="#" onclick="openMessageBox(${dialog["uid"]})" class="row ${dialog["isRead"] ? '' : 'font-weight-bold'}">
              <img src="${dialog["photo"]}" class="col-sm-3" width="40px" height="40px">
              <span class="col-sm-9">
                <span>${dialog["full_name"]}</span><br>
                <span style="font-size:13px" class="text-muted">@${dialog["username"]}</span>
              </span>
            </a>
          </span>
          <span class="col-sm-3"><button id="delete-dialog-button" class="btn btn-danger">Delete</button></span>
        </span>
        `;
        modalBody.appendChild(element);
      });  
    }

    this.setModal(this.generalModal, "Messages", modalBody, true);
    $("#general-modal").modal("show");
  }

  showMessages(msgList, currentUser, otherUser){
    this.closeAllModals();
    
    let modalBody = document.createElement("div");
    modalBody.setAttribute("uid", otherUser["uid"]);
    if(msgList.length == 0){
      modalBody.textContent = "You don't have any message with this user :(";
    }
    else{
      msgList.forEach(message => {
        let element = document.createElement("span");
        element.className = `msg ${(message["sender_id"] == currentUser["uid"]) ? 'outgoing-msg' : 'incoming-msg'}`;
        element.setAttribute("mid", message["mid"]);
  
        element.innerHTML =
        `
          ${message["message"]}
        `;
        
        modalBody.insertAdjacentElement("afterbegin", element);
      });  
    }

    this.setModal(this.messageModal, otherUser["full_name"], modalBody);

    $("#message-modal").modal("show");
  }

  showPreviousMessages(msgList, currentUser){
    msgList.forEach(message => {
      let element = document.createElement("span");
      element.className = `msg ${(message["sender_id"] == currentUser["uid"]) ? 'outgoing-msg' : 'incoming-msg'}`;
      element.setAttribute("mid", message["mid"]);

      element.innerHTML =
      `
        ${message["message"]}
      `;
      let container = this.messageModal.querySelector(".modal-body").firstElementChild;
      container.insertAdjacentElement("afterbegin", element);
    });  
  }


  addMessage(mid, message, type){
    let element = document.createElement("span");
    element.className = `msg ${type}-msg`;
    element.setAttribute("mid", mid);

    element.textContent = message;

    this.messageModal.querySelector(".modal-body").firstElementChild.appendChild(element);
    this.messageModal.querySelector("textarea").value = "";

    this.gotoBottom(this.messageModal.querySelector(".modal-body"));
  }


  setModal(modal, title, body, hideFooter = false){
    let modalTitle = modal.querySelector(".modal-title");
    let modalBody = modal.querySelector(".modal-body");

    modalTitle.innerText = title;

    modalBody.innerHTML = body.outerHTML;

    this.gotoBottom(modalBody);

    if(hideFooter){
      modal.querySelector(".modal-footer").style.display = "none";
    }
    else{
      modal.querySelector(".modal-footer").style.display = "block";
    }
  }

  gotoBottom(element){
    //Change this later
    setTimeout(() => {
      element.scrollTo(0, element.scrollHeight);
    }, 350);
  }

  closeAllModals(){
    $("#general-modal").modal("hide");
    $("#message-modal").modal("hide");
  }
}