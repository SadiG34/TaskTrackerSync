from django.db import models


class TaskYougile(models.Model):
    dict_info = models.CharField(max_length=5000, blank=True, null=True)

class TaskPlanfix(models.Model):
    dict_info = models.CharField(max_length=5000, blank=True, null=True)

    # title = models.CharField(max_length=255, null=True)
    # timestamp = models.DateTimeField(null=True)
    # columnId = models.IntegerField(null=True)
    # description = models.TextField(null=True)
    # archived = models.BooleanField(null=True)
    # completed = models.BooleanField(null=True)
    # createdBy = models.IntegerField(null=True)
    # stickers = models.JSONField(null=True)
    # assigned = models.IntegerField(null=True)
    # stopwatch = models.JSONField(null=True)
    # timeTracking = models.JSONField(null=True)

