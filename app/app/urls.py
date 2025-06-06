"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from appaccount.api import router as account_router
from appaccount.services.auths import BearerTokenAuth
from appdemo.api import router as demo_router  # remove when using this template
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Swagger

from app import views

api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))
api.add_router("/account", account_router)
api.add_router(
    "/demo", demo_router, auth=BearerTokenAuth()
)  # remove when using this template

urlpatterns = [
    path("", views.index, name="index"),  # Add root URL path to show the index
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
