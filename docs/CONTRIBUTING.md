#  CONTRIBUTING GUIDELINE

First of all, thank you for considering contributing to devSeater. With your contributions, devSeater can be a great platform for developers. In first place, the main purpose of this project is collabrate with people and building new things together. Therefore, you are in the right place.

  

##  Kinds of Contributions

We are open to any type of contributions. But in terms of giving ideas, we can say the followings:

- Document Editing and Writing

- Testing Application

- Finding Bugs

- Making Suggestions about Codebase and Project

- Code Shipping

  

To become an active contributor, you can request the open positions(seaters) on devSeater project page in devSeater.com:

[devSeater project page](https://devseater.com/p/devSeater)

  

##  How to Set up and Run the Project on Local Server?

  

**1. First of all, clone the project**

(If you don't have git command line tools on your computer, before install it)

  

```git clone https://github.com/metinorak/devSeater```

  

**2. Open the project folder in command line and create a virtual environment**

  

```python3 -m venv venv```

  

**3. Activate the virtual environment**

  

*On Windows:*

```venv\Scripts\activate.bat ```

  

*On Linux and Unix:*

```source venv/bin/activate ```

  

**4. Install required packages**

```pip install -r requirements.txt```

  

**5. Run your mysql-server and create a mysql database and update the configuration file.**

Configuration file is in `project/config.py`

  

**6. In the root directory of the project, run the following command to migrate the database schema**

```yoyo apply --database mysql://[username]:[password]@localhost/[database_name] ./migrations```

  

Write your database credentials instead of [username], [password] and [database_name] fields.

  

**7. Run the project**

```python3 start.py ```

  

You'll see the application outputs and local adress of the application. Open that address on your browser.

  

**8. Create a test user from home page of the website**

  

**9. Change the `isEmailVerified` column of the test user from your mysql client tool.**

User records are in the `user` table. Update `isEmailVerified` value to `1`.

Because, for now, login to this application without the email verification is restricted.

  

**10. You can login to the website after the updating `isEmailVerified` field.**
