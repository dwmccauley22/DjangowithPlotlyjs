# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 15:22:54 2022

@author: dwmccauley
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.plot, name='plot'),
]