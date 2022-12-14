# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 15:22:54 2022

@author: dwmccauley
"""

from django.urls import path

from . import views
app_name = 'graph'
urlpatterns = [
    path('', views.plot,name='plot'),
    path('spc/', views.plot,name='spc'),
    path('multigraph/', views.multigraph,name='multigraph'),
    path('contour/', views.contour,name='contour'),
    path('csv_upload/', views.csv_upload,name='csv_upload')
]