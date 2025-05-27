from django import forms


class Fieldset(object):
    def __init__(self, title, fields):
        self.title = title
        self.fields = fields

    def __iter__(self):
        for field in self.fields:
            yield field


class FormWithFormsets(forms.Form):
    def fieldsets(self):
        meta = getattr(self, 'Meta')

        if not meta or not meta.fieldsets:
            return

        for name, data in meta.fieldsets:
            yield Fieldset(
                title=name,
                fields=(self[f] for f in data['fields']),
            )


class StatisticsForm(forms.Form):
    choices = []
    x_attribute = forms.ChoiceField(choices=choices)
    y_attribute = forms.ChoiceField(choices=choices)

    def clean(self):
        cleaned_data = super().clean()
        x_attribute = cleaned_data.get('x_attribute')
        y_attribute = cleaned_data.get('y_attribute')
        if x_attribute and y_attribute:
            if x_attribute == y_attribute:
                raise forms.ValidationError("Выберите разные атрибуты для X и Y.")