from django.shortcuts import render


def index(request):
    """
    Simple view to render the index page with links to admin and API docs
    """
    return render(request, "index.html")
