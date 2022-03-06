from django.db import models

# Create your models here.
class Queries(models.Model):
    question_url_slug = models.TextField(null = True)
    question_id = models.IntegerField(null = True)
    difficulty = models.TextField(null = True)
    content = models.TextField(null = True)
    similar_questions = models.TextField(null = True)
    topics = models.TextField(null = True)
    videos = models.TextField(null = True)
    title = models.TextField(null = True)