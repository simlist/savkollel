from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def profile(request):
#change to home
    return redirect('/nlaws/')