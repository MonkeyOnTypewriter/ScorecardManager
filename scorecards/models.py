from django.db import models

# Create your models here.

class Scorecard(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name


class ScorecardTier(models.Model):
    scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=2)
    def __str__(self):
        return self.name