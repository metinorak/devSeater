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

  //USER POSTS
  async lastUserPosts(uid){
    return this.request.get(this.url + `user-posts?uid=${uid}`);
  }

  async previousUserPosts(uid, upid){
    return this.request.get(this.url + `user-posts?uid=${uid}&upid=${upid}`);
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

  async updateUserPost(upid, post){
    return this.request.put(this.url + `user-posts?upid=${upid}`, post);
  }

  async updateUserPhoto(uid, file){
    return this.request.upload(this.url + `users/${uid}/photo`, file);
  }

  async updateUserFullName(name){
    return this.request.put(this.url + `users/full-name?full-name=${name}`)
  }

  async updateUserBio(bio){
    return this.request.put(this.url + `users/bio`, {bio: bio});
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


  async follow(uid){
    return this.request.get(this.url + `follow/${uid}`);
  }

  async unFollow(uid){
    return this.request.get(this.url + `unfollow/${uid}`);
  }

  async userSeaters(uid=null){
    return this.request.get(this.url + `users/${uid}/seaters`);
  }

  async userSkills(uid=null){
    if(uid == null){
      return this.request.get(this.url + `user-skills`);
    }
    else{
      return this.request.get(this.url + `user-skills?uid=${uid}`);
    }
  }

  async addUserSkill(skill){
    return this.request.post(this.url + `user-skills?skill=${skill}`);
  }

  async deleteUserSkill(skid){
    return this.request.delete(this.url + `user-skills?skid=${skid}`);
  }

  async userLinks(uid=null){
    if(uid == null){
      return this.request.get(this.url + `user-links`);
    }
    else{
      return this.request.get(this.url + `user-links?uid=${uid}`);
    }
  }

  async addUserLink(link){
    return this.request.post(this.url + `user-links`, link);
  }

  async deleteUserLink(ulid){
    return this.request.delete(this.url + `user-links?ulid=${ulid}`);
  }

  //PROJECT POSTS
  async sendProjectPost(pid, post){
    return this.request.post(this.url + `projects/${pid}/posts`, {post: post});
  }

  async deleteProjectPost(ppid){
    return this.request.delete(this.url + `projects/no-matter/posts?ppid=${ppid}`);
  }

  async updateProjectPost(ppid, post){
    return this.request.put(this.url + `projects/no-matter/posts?ppid=${ppid}`, post);
  }

  async lastProjectPosts(pid){
    return this.request.get(this.url + `projects/${pid}/posts`);
  }

  async previousProjectPosts(pid, ppid){
    return this.request.get(this.url + `projects/${pid}/posts?ppid=${ppid}`);
  }

  async likeProjectPost(ppid){
    return this.request.get(this.url + `project-posts/${ppid}/like`);
  }

  async unlikeProjectPost(ppid){
    return this.request.get(this.url + `project-posts/${ppid}/unlike`);
  }

  async projectPostLikeNumber(ppid){
    return this.request.get(this.url + `project-posts/${ppid}/likes/number`);
  }

  async projectPostCommentNumber(ppid){
    return this.request.get(this.url + `project-posts/${ppid}/comments/number`);
  }

  async projectPostComments(ppid, number = 2){
    return this.request.get(this.url + `project-posts/${ppid}/comments?number=${number}`);
  }

  async previousProjectPostComments(ppid, ppcid, number = 2){
    return this.request.get(this.url + `project-posts/${ppid}/comments?ppcid=${ppcid}&number=${number}`);
  }

  async likeProjectPostComment(ppcid){
    return this.request.get(this.url + `project-posts/comments/${ppcid}/like`);
  }

  async unlikeProjectPostComment(ppcid){
    return this.request.get(this.url + `project-posts/comments/${ppcid}/unlike`);
  }

  async projectPostCommentLikeNumber(ppcid){
    return this.request.get(this.url + `project-posts/comments/${ppcid}/likes/number`);
  }

  async sendProjectPostComment(ppid, comment){
    return this.request.post(this.url + `project-posts/${ppid}/comments`, {comment: comment});
  }

  async deleteProjectPostComment(ppcid){
    return this.request.delete(this.url + `project-posts/no-matter/comments?ppcid=${ppcid}`);
  }

  //PROJECTS
  async project(pid){
    return this.request.get(this.url + `projects/${pid}`);
  }

  async updateProjectPhoto(pid, file){
    return this.request.upload(this.url + `projects/${pid}/photo`, file);
  }

  async updateProjectName(pid, name){
    return this.request.put(this.url + `projects/${pid}/name/${name}`);
  }

  async updateProjectShortDescription(description){
    return this.request.put(this.url + `projects/${pid}/short-description`, {description: description});
  }

  async updateProjectFullDescription(description){
    return this.request.put(this.url + `projects/${pid}/full-description`, {description: description});
  }

  async createSeater(pid){
    return this.request.post(this.url + `projects/${pid}/seaters`, seater)
  }

  async seater(sid){
    return this.request.get(this.url + `seaters/${sid}`);
  }

  async projectEmptySeaters(pid){
    return this.request.get(this.url + `projects/${pid}/seaters/empty`);
  }

  async projectFilledSeaters(pid){
    return this.request.get(this.url + `projects/${pid}/seaters/filled`);
  }

  async projectMembers(pid){
    return this.request.get(this.url+ `projects/${pid}/members`);
  }

  async isProjectMember(pid, uid){
    return this.request.get(this.url + `projects/${pid}/members/check/${uid}`)
  }

  async isProjectAdmin(pid, uid){
    return this.request.get(this.url + `projects/${pid}/admins/check/${uid}`)
  }

  async projectLinks(pid){
    return this.request.get(this.url + `projects/${pid}/links`);
  }

  async addProjectLink(pid, link){
    return this.request.post(this.url + `projects/${pid}/links`, link);
  }

  async deleteProjectLink(plid){
    return this.request.delete(this.url + `projects/no-matters/links?plid=${plid}`);
  }

}