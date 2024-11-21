"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from ninja import NinjaAPI
from pet.routers.pets_router import router as pets_router
from member.routers.users_router import router as users_router

api = NinjaAPI(csrf=True)
api.add_router("/pet", pets_router)
api.add_router("/users", users_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
]
