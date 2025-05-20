from django import forms
# import magic


class ImportForm(forms.Form):
    import_file = forms.FileField()

    # def clean_import_file(self):
    #     import_file = self.cleaned_data.get('import_file')
