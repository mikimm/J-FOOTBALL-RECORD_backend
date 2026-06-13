from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.shortcuts import render, redirect
from django.conf import settings
from django.db import transaction
from django.contrib.auth import login as auth_login
from jfootball_record.forms import SignUpForm


class SignupView(View):
    def get(self, request, *args, **kwargs):
        context = {'form': SignUpForm()}
        return render(request, 'signup.html', context)

    def post(self, request, *args, **kwargs):
        print(request)
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup.html', {'form': form})
        user = self.register_user(form)
        auth_login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL) 
    
    @transaction.atomic
    def register_user(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        print(user)
        return user
