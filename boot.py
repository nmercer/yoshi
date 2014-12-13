from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
    from wtforms.validators import Required

def create_app(configfile=None):
    app = Flask(__name__)
    Bootstrap(app)

    @app.route('/')
    def index():

