from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from .forms import RegistrationForm

class Home(View):
    def get(self, request):
        return redirect('/courses')
    
class SignUp(View):
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return self.render_sign_up(request, {'form': form})
    
    def get(self, request):
        form = RegistrationForm()
        return self.render_sign_up(request, {'form': form})

    def render_sign_up(self, request, context):
        return render(request, 'registration/sign_up.html', context)