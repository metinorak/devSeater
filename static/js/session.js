class Session{
  static createSession(user){
    sessionStorage.setItem("currentUser", JSON.stringify(user));
  }

  static getCurrentUser(){
    return JSON.parse(sessionStorage.getItem("currentUser"));
  }

  static destroySession(){
    sessionStorage.removeItem("currentUser");
  }
}