# Generated by Django 5.1.2 on 2024-11-14 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobListing',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('job_title', models.CharField(max_length=255)),
                ('job_location', models.CharField(max_length=255)),
                ('date_posted', models.DateTimeField()),
                ('source_link', models.URLField(max_length=500)),
                ('hiring_organization', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'JobListings',
            },
      
        )]
