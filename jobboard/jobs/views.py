from django.shortcuts import render, get_object_or_404
from .models import Jobs
from django.core.paginator import Paginator

def job_listings(request):
    """
    Display all job listings with optional search filters, pagination, and view mode (grid or list).
    """
    # Get search parameters and view mode from the request
    job_title = request.GET.get('job_title', '')  # Default to an empty string if not provided
    location = request.GET.get('location', '')
    view_mode = request.GET.get('view_mode', 'list')  # Default to list view
    page_number = request.GET.get('page', 1)

    # Start with all jobs
    jobs_query = Jobs.objects.all()

    # Apply filters if search parameters are provided
    if job_title:
        jobs_query = jobs_query.filter(job_title__icontains=job_title)  # Case-insensitive match
    if location:
        jobs_query = jobs_query.filter(job_location__icontains=location)  # Case-insensitive match

    # Set items per page based on view mode
    items_per_page = 20 if view_mode == 'grid' else 10

    # Apply pagination
    paginator = Paginator(jobs_query, items_per_page)
    try:
        jobs = paginator.get_page(page_number)
    except (EmptyPage, InvalidPage):
        jobs = paginator.get_page(1)  # Fall back to the first page

    # Render the template with paginated jobs
    context = {
        'jobs': jobs,
        'view_mode': view_mode,
        'job_title': job_title,
        'location': location,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, job_id):
    """
    Display the details of a single job posting.
    """
    job = get_object_or_404(Jobs, id=job_id)  # Fetch job by ID or return 404 if not found
    return render(request, 'jobs/job_detail.html', {'job': job})


def about_page(request):
    """
    Display the about page.
    """
    return render(request, 'jobs/about.html')
