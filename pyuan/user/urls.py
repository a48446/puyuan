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
    path('', views.index),                                        
    path('register/', views.register),    #串完
    path('register/check/',views.registercheck),     #串完                     
    path('auth/', views.login),      #串完                              
    path('logout/', views.logout),    #串完                             
    path('verification/send/', views.send),   #串完
    path('verification/check/', views.check),  #串完                                
    path('password/forgot/', views.forgot),   #串完                             
    path('password/reset/', views.reset),      #串完                             
    path('user/default/', views.default),
    # path('user/privacy-policy/',views.privacy_policy),  # 13.隱私權聲明 FBLogin                          
    path('user/', views.sett),   
    path('user/sett/', views.userdata),                   #串完 
    path('user/badge/',views.badge),            #串完  
    path('news/', views.newnews),                         #---------------------         
    path('user/medical/', views.Medical_information),                 
    path('user/a1c/', views.showHbA1c),              #上傳ok 展示未知             
    path('user/drug-used/', views.drug),            #上傳ok 展示未知
    path('notification/', views.notification),      #-----
    path('share/', views.share),                       #串完
    path('share/<int:relation_type>', views.share_check),     #串完
]



