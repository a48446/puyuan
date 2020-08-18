"""puyuanAPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('user/blood/pressure/', views.blood_pressure),     #串完
    path('user/weight/', views.body_weight),    #串完
    path('user/blood/sugar/', views.blood_sugar),    #串完
    path('user/last_upload/', views.last_upload),
    path('user/records/', views.records),
    path('user/diary/', views.diary_list),    #串完
    path('user/diet/', views.diary_diet),     
    path('user/care/', views.care),     #串完
]

