from django.shortcuts import render

# Create your views here.
def plot(request):
    return render(request, 'graph/plot.html')