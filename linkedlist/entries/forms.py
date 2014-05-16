"""
LinkedList entry forms
"""

from flask_wtf import Form
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, URL

__all__ = ["NewEntryForm"]


class NewEntryForm(Form, EntryFormMixin):
    url = URLField(validators=[DataRequired(), URL()])
