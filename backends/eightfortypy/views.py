from django.shortcuts import render
from django.views.generic import * 
from django.db import models

from eightfortypy.models import * 
# Create your views here.

def index(request):
    return render(request,"main/index.html")


class MusicList(ListView):
    model = Song 
    template_name = 'main/list_page.html'
    context_object_name = "song"
    paginate_by = 20
    
    
    