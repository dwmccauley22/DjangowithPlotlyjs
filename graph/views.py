from django.shortcuts import render

# Create your views here.
def plot(request):
    return render(request, 'graph/plot.html')
def multigraph(request):
    return render(request, 'graph/multiplot.html')
def contour(request):
    return render(request, 'graph/contour.html')