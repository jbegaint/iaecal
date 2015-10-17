# forms.py

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from widgets import AngularJSTextInput, AngularJSPasswordInput


class UserInfoForm(Form):
    username = StringField(
        "Nom d'utilisateur",
        validators=[DataRequired()],
        widget=AngularJSTextInput(),
    )
    password = PasswordField(
        "Mot de passe",
        validators=[DataRequired()],
        widget=AngularJSPasswordInput(),
    )
