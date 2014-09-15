from django.forms import ModelForm
from api.models import Play
from django import forms

class PlayForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Play
        exclude = ['gamekey', 'points']

    def __init__(self, away_team, home_team, *args, **kwargs):
        super(PlayForm, self).__init__(*args, **kwargs)
        self.fields['team'] = forms.ChoiceField(required=False,
            choices=(('', '---------'), (away_team, away_team), (home_team, home_team)))