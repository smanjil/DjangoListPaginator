# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from users.forms import (
    RegisterForm,
    LoginForm
)

# Create your views here.

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'redirect')
        return reverse('users:login')

class LoginView(FormView):
    form_class = LoginForm
    model = User
    template_name = 'users/login.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        username = form.data['username']
        password = form.data['password']

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/genericviews/')
        else:
            messages.add_message(self.request, messages.ERROR, 'redirect')
            return HttpResponseRedirect('/users/login')