from django import forms
from .utils import get_team_choices

class PredictionForm(forms.Form):
    home_team = forms.ChoiceField(choices=[], label="Home Team")
    away_team = forms.ChoiceField(choices=[], label="Away Team")

    def __init__(self, *args, **kwargs):
        super(PredictionForm, self).__init__(*args, **kwargs)
        choices = get_team_choices()
        self.fields['home_team'].choices = choices
        self.fields['away_team'].choices = choices
