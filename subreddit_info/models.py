from django.db import models

class Subreddit(models.Model):
    """
    Subreddit object containing date,
    name, and score.
    """
    index = models.IntegerField(primary_key=True)
    date = models.DateField(auto_now_add=True, blank=True)
    name = models.CharField(max_length=200, default='None')
    score = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns a string representation of
        Subreddit object. 
        """
        return f"Name: {self.name}, Date: {self.date}, Score: {self.score}"

    class Meta:
        db_table = "subreddit_data"