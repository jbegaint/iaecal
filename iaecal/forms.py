# forms.py

from flask.ext.wtf import Form as BaseForm
from flask.ext.babel import lazy_gettext as _
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from utils import check_credentials
from widgets import AngularJSTextInput, AngularJSPasswordInput


class Form(BaseForm):
    """
    Add non-field errors support to `Form`.
    """
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.non_field_errors = []

    @property
    def errors(self):
        errors = super(Form, self).errors
        if self.non_field_errors:
            errors['non_field_errors'] = self.non_field_errors
        return errors


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

    def validate(self):
        if not super(UserInfoForm, self).validate():
            return False

        # Check if the credentials are valid
        if not check_credentials(self.username.data, self.password.data):
            # It seems that wtforms don't support non-field errors...
            self.non_field_errors.append(_("Invalid username or password"))
            return False

        return True
