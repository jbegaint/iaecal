# widgets.py

from wtforms.widgets import TextInput, PasswordInput


class AngularJSInput(object):
    def __call__(self, field, **kwargs):
        for key in list(kwargs):
            if key.startswith('ng_'):
                kwargs['ng-' + key[3:]] = kwargs.pop(key)
        kwargs['server-error'] = ''
        return super(AngularJSInput, self).__call__(field, **kwargs)


class AngularJSTextInput(AngularJSInput, TextInput):
    pass


class AngularJSPasswordInput(AngularJSInput, PasswordInput):
    pass
