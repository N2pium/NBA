from django.db import models

# Create your models here.

class matchup(models.Model):
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    date = models.DateField()

 
    
class predictionResult(models.Model):
    matchup = models.ForeignKey(matchup, on_delete=models.CASCADE)
    predicted_winner = models.CharField(max_length=100)
    confidence = models.FloatField()

  