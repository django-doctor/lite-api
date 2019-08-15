import six
from django.utils.translation import ugettext_lazy as _
from rest_framework.fields import Field, iter_options, to_choices_dict, flatten_choices_dict


class KeyValueChoiceField(Field):
    default_error_messages = {
        'invalid_choice': _('"{input}" is not a valid choice.')
    }
    html_cutoff = None
    html_cutoff_text = _('More than {count} items...')

    def __init__(self, choices, **kwargs):
        self.choices = choices
        self.html_cutoff = kwargs.pop('html_cutoff', self.html_cutoff)
        self.html_cutoff_text = kwargs.pop('html_cutoff_text', self.html_cutoff_text)

        self.allow_blank = kwargs.pop('allow_blank', False)

        super(KeyValueChoiceField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        try:
            return self.choice_strings_to_values[six.text_type(data)]
        except KeyError:
            self.fail('invalid_choice', input=data)

    def to_representation(self, value):
        if value in ('', None):
            return value
        return {
            'key': six.text_type(value),
            'value': self.choices[value]
        }

    def iter_options(self):
        """
        Helper method for use with templates rendering select widgets.
        """
        return iter_options(
            self.grouped_choices,
            cutoff=self.html_cutoff,
            cutoff_text=self.html_cutoff_text
        )

    def _get_choices(self):
        return self._choices

    def _set_choices(self, choices):
        self.grouped_choices = to_choices_dict(choices)
        self._choices = flatten_choices_dict(self.grouped_choices)

        # Map the string representation of choices to the underlying value.
        # Allows us to deal with eg. integer choices while supporting either
        # integer or string input, but still get the correct datatype out.
        self.choice_strings_to_values = {
            six.text_type(key): key for key in self.choices
        }

    choices = property(_get_choices, _set_choices)