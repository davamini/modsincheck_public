from django.db import models
# Create your models here.

class Mod(models.Model):
    """
    Mod object containing name, subreddit, 
    score, and date attributes.
    """
    index = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, default='None')
    subreddit = models.CharField(max_length=200, default='None')
    score = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True, blank=True)
    subreddits_moderated = models.CharField(max_length=200, default='None')
    account_created = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        """
        Returns string representation of Mod object, 
        i.e. name, subreddit, score, date.
        """
        return f'Name: {self.name}, Subreddit: {self.subreddit}, Score: {self.score}, Last Updated: {self.date}, Account Created: {self.account_created}'

    class Meta:
        db_table = "mod_data"