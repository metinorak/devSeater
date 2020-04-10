from flask import Flask

app = Flask(__name__)
app.secret_key = "my_secret_key"

import project.controllers