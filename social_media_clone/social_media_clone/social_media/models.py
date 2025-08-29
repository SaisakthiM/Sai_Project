# posts/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = [(UPVOTE, 'Upvote'), (DOWNVOTE, 'Downvote')]

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    
    class Meta:
        unique_together = ('post', 'user')  # one vote per user per post
