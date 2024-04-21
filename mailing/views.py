from django.shortcuts import redirect
from django.contrib import messages
from django.views import View
from .forms import SubscribeForm

class SubscribeView(View):
    def post(self, request):
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have subscribed successfully!')
        else:
            messages.error(request, 'Please enter a valid email address.')
        return redirect('home')