class DevSeater{

  constructor() {
    this.url = "http://localhost:5000/private-api/"
    this.request = new Request()
  }
  
  async generalSearch(query){
    return this.request.get(this.url + "q/" + query)
  }

  async newDialogNumber(){
    return this.request.get(this.url + "messages/new-dialog-number");
  }

  async newFollowingPostNumber(upid){
    return this.request.get(this.url + "new-following-post-number?upid=" + upid);
  }

  async newNotificationNumber(){
    return this.request.get(this.url + "notifications/new/number");
  }

  async newFollowingPosts(upid){
    return this.request.get(this.url + "new-following-posts?upid=" + upid);
  }

  async previousFollowingPosts(upid){
    return this.request.get(this.url + `previous-following-posts?upid=${upid}`);
  }

  async sendUserPost(post){
    return this.request.post(this.url + "user-posts", {post: post});
  }

  async currentUser(){
    return this.request.get(this.url + "current-user");
  }

  async deleteUserPost(upid){
    return this.request.delete(this.url + "user-posts?upid=" + upid.trim());
  }

  async likeUserPost(upid){
    return this.request.get(this.url + `user-posts/${upid}/like`);
  }

  async unlikeUserPost(upid){
    return this.request.get(this.url + `user-posts/${upid}/unlike`);
  }

  async userPostLikeNumber(upid){
    return this.request.get(this.url + `user-posts/${upid}/likes/number`);
  }

  async userPostCommentNumber(upid){
    return this.request.get(this.url + `user-posts/${upid}/comments/number`);
  }

  async userPostComments(upid, number = 2){
    return this.request.get(this.url + `user-posts/${upid}/comments?number=${number}`);
  }


  
  async likeUserPostComment(upcid){
    return this.request.get(this.url + `user-posts/comments/${upcid}/like`);
  }

  async unlikeUserPostComment(upcid){
    return this.request.get(this.url + `user-posts/comments/${upcid}/unlike`);
  }

  async userPostCommentLikeNumber(upcid){
    return this.request.get(this.url + `user-posts/comments/${upcid}/like-number`);
  }

  async sendUserPostComment(upid, comment){
    return this.request.post(this.url + `user-posts/${upid}/comments`, {comment: comment});
  }

  async previousUserPostComments(upid, upcid, number = 2){
    return this.request.get(this.url + `user-posts/${upid}/comments?upcid=${upcid}&number=${number}`);
  }

  async deleteUserPostComment(upcid){
    return this.request.delete(this.url + `user-posts/no-matter/comments?upcid=${upcid}`);
  }
}