from django.urls import path,include

import checkerapp.views

urlpatterns =[
    path(r'checkerapp/checkerarchive/',checkerapp.views.checker_archive, name='checker_archive'),
    path('',checkerapp.views.index, name='index'),
    path('checkerapp/checkerpost/',checkerapp.views.checker_post,name='checker_post'),
    ]