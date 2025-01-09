from django.db import models

class Jobs(models.Model):
    # Define fields that match your existing database columns
    id = models.IntegerField(primary_key=True)
    job_title = models.CharField(max_length=255)
    job_location = models.CharField(max_length=255)
    date_posted = models.DateField()
    source_link = models.URLField(max_length=500)
    hiring_organization = models.CharField(max_length=255)

    class Meta:
        # Specify the exact database table name
        db_table = 'JobListings'

    def __str__(self):
        return self.job_title
