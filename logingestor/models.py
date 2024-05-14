from django.db import models

# Create your models here.
class Log(models.Model):
    LEVEL_CHOICES = [
        ('info', 'Info'),
        ('error', 'Error'),
        ('success', 'Success')
    ]
    
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    log_string = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.timestamp} - {self.level} - {self.log_string} - {self.source}"
