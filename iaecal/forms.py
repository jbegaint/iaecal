# forms.py

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext as _
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from widgets import AngularJSTextInput, AngularJSPasswordInput


class UserInfoForm(Form):
    username = StringField(
        _("Username"),
        validators=[DataRequired()],
        widget=AngularJSTextInput(),
    )
    password = PasswordField(
        _("Password"),
        validators=[DataRequired()],
        widget=AngularJSPasswordInput(),
    )
