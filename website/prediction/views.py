from django.shortcuts import render
from .forms import PredictionForm
from .utils import predict_matchup, get_todays_games, get_week_schedule
from datetime import datetime


def index(request):
    """Render the home page using the prediction/index.html template."""
    todays_games = get_todays_games()
    upcoming_games = get_week_schedule()
    
    context = {
        "now": datetime.now(),
        "todays_games": todays_games,
        "upcoming_games": upcoming_games
    }
    return render(request, "prediction/index.html", context)

def about(request):
    """Render the about page using the prediction/about.html template."""
    context = {"now": datetime.now()}
    return render(request, "prediction/about.html", context)

def prediction_view(request):
    result = None
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            home_team = form.cleaned_data['home_team']
            away_team = form.cleaned_data['away_team']
            result = predict_matchup(home_team, away_team)
    else:
        form = PredictionForm()
    
    return render(request, 'prediction/predict.html', {'form': form, 'result': result})

