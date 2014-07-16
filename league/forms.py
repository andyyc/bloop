from django import forms
from league.models import League
from gm.models import Manager

class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ('name',)

class JoinLeagueForm(forms.Form):
    lid = forms.CharField(max_length=6)

class GeneralManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ('name',)

