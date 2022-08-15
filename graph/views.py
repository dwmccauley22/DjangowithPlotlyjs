from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib import messages
import logging
import pandas
from src import srccalculate
# Create your views here.
def plot(request):
    return render(request, 'graph/plot.html')
def multigraph(request):
    return render(request, 'graph/multiplot.html')
def contour(request):
    return render(request, 'graph/contour.html')
def csv_upload(request):
    df_json = (pandas.DataFrame()).to_json(orient = 'values')
    if request.method == "GET":
        if(df_json != "[]"):
            return render(request, "graph/csv_upload.html", {'df' : df_json})
        else:
            return render(request, "graph/csv_upload.html")
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("graph:csv_upload"))
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("graph:csv_upload"))
        #print(pandas.read_csv(csv_file))
        df = pandas.read_csv(csv_file)
        df_json = df.to_json(orient = 'values')
        print(df_json)
        df_violations = srccalculate(df,0)
        df_v_json = df_violations.to_json(orient = 'values')
       # print(csv_file.read().decode("utf-8"))
        #file_data = csv_file.read().decode("utf-8")	
        #print(file_data.split("\n"))
        return render(request, "graph/csv_upload.html", {'df' : df_json, 'dfv' : df_v_json})
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
        df_json = (pandas.DataFrame()).to_json(orient = 'values')
    
    return HttpResponseRedirect(reverse("graph:csv_upload"))