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
    path('code/', views.friend_code),    #串完
    path('list/', views.friend_list),    #串完
    path('requests/', views.friend_requests),    #串完
    path('send/', views.friend_send),    #串完
    path('<int:friend_data_id>/accept/', views.friend_accept),    #串完
    path('<int:friend_data_id>/refuse/', views.friend_refuse),    #串完
    path('<int:friend_data_id>/remove/', views.friend_remove),    #串完
    path('results/', views.friend_results),
    path('remove/', views.friend_remove_more),    #串完
]

