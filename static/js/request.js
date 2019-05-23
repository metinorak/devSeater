class Request{

  async get(url){
    const response = await fetch(url);
    const responseData = await response.json();

    return responseData;
  }

  async post(url, data){
    const response = await fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });

    const responseData = await response.json();

    return responseData;
  }

  async delete(url){
    const response = await fetch(url, {
      method: "DELETE"
    });

    return response;
  }

  async put(url, data){

    const response = await fetch(url, {
      method: "PUT",
      body: JSON.stringify(data),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });

    const responseData = await response.json();

    return responseData;
  }


}