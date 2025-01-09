from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_listings, name='jobs'),  # Main jobs page
    path('<int:job_id>/', views.job_detail, name='job_detail'),  # Job detail view
    path('about/', views.about_page, name='about'),  # About page
]

