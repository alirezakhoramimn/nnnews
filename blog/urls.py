#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:14:24 2020

@author: alirezakh
"""
from .views import (PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
    				) 
from . import views 
from django.urls import path
from .feeds import LatestPostsFeed

urlpatterns = [
	path('', views.post_list, name='home'),
    path('<slug:slug>', views.post_detail_view, name='post_detail'),
    path("feed/rss/", LatestPostsFeed(), name="post_feed"),
    path('tag/<slug:slug>/', views.tagged, name='tagged'),
    #path('posts/detail/<int:pk>/'.post_detail(),name = 'blog-detail-comment' ),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    # Updating every post that we have.
    path('post/<slug:slug>/update', PostUpdateView.as_view(), name='post-update'),
    # This is gonna delete the post
    path('post/<slug:slug>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name="user-posts"),
]
