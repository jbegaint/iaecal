# iaecal/serializers.py

from flask.json import JSONEncoder as BaseEncoder
from speaklater import _LazyString


class JSONEncoder(BaseEncoder):
    """
    Custom JSONEncoder for encoding json data.
    Necessary when returning translated data via jsonify or flashing it.
    """
    def default(self, o):
        if isinstance(o, _LazyString):
            return unicode(o)
        return super(JSONEncoder, self).default(o)
