# Generated by Django 5.1.2 on 2024-12-13 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_joblisting_delete_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('job_title', models.CharField(max_length=255)),
                ('job_location', models.CharField(max_length=255)),
                ('date_posted', models.DateField()),
                ('source_link', models.URLField(max_length=500)),
                ('hiring_organization', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'JobListings',
            },
        ),
        migrations.DeleteModel(
            name='Job',
        ),
        migrations.DeleteModel(
            name='JobListing',
        ),
    ]
