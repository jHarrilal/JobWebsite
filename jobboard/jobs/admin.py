# jobs/admin.py

from django.contrib import admin
from .models import Jobs  # Adjust if the model is named JobListing

# Register your model with the Django admin
admin.site.register(Jobs)
