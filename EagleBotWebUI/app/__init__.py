from flask import Flask

app = Flask(__name__)

from EagleBotWebUI.app import routes