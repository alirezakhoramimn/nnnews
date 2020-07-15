#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:28:24 2020

@author: alirezakh
"""
from django import forms 
from .models import Comment, Post

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title','content','tags')


class CommentForm(forms.ModelForm):
	name = forms.CharField() 
	body = forms.CharField()

	class Meta:
		model = Comment
		fields = ('name', 'email', 'body')