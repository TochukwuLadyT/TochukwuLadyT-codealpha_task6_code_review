from django import forms
from codemirror2.widgets import CodeMirrorEditor


class ReviewForm(forms.Form):
    code = forms.CharField(widget=CodeMirrorEditor(options={'mode': 'python'}))

