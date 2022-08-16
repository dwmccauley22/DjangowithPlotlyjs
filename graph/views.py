from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib import messages
import logging
import pandas

def srccalculate(data,col):
    stdv = data.std()
    mean = data.mean()
    sigma1plus = float(mean + stdv)
    sigma1min = float(mean - stdv)
    sigma2plus = float(mean + (stdv*2))
    sigma2min = float(mean - (2*stdv))
    sigma3plus = float(mean + (stdv*3))
    sigma3min = float(mean - (3*stdv))
    print("std:" + str(stdv))
    print("mean: " + str(mean))
    print("+/- sigma 1 = " + str(float(mean + stdv)) + " " +str(float(mean - stdv)))
    print("+/- sigma 2 = " + str(float(mean + (stdv*2))) + " " +str(float(mean - (2*stdv))))
    print("+/- sigma 3 = " + str(float(mean + (stdv*3))) + " " +str(float(mean - (3*stdv))))
    (vs1p,vs1m,vs2p,vs2m) = (0,0,0,0)
    v = []
    win = pandas.DataFrame()
    win= data.loc[0:4]
    #see if violates 1 sigma
    for x in range(1,len(data)-4,1):
        vs1p = 0
        vs1m = 0
        for y in range(0,len(win),1):
        
            if(win.iat[y,col] > sigma1plus).all():
                vs1p +=1
            if (win.iat[y,col] < sigma1min).all():
                vs1m +=1
            if (win.iat[y,col] > stdv).all():
                vs1m=0
            if (win.iat[y,col] < stdv).all():
                vs1p=0
            
        print(win)   
        print("vs1p: " + str(vs1p) + " vs1m: " + str(vs1m))
        print("x pass # %d : ",x)
        
        if(vs1p >= 4) or (vs1m >= 4):
            for z in range(0,len(win),1):
                v.append([win.iat[z,col],x+z])
        win = data.loc[x+1:x+5]
    #see if violates 2 sigma
    win= data.loc[0:2]
    for x in range(1,len(data)-2,1):
        vs2p = 0
        vs2m = 0
        for y in range(0,len(win),1):
        
            if(win.iat[y,col] > sigma2plus).all():
                vs2p +=1
            if (win.iat[y,col] < sigma2min).all():
                vs2m +=1
            if (win.iat[y,col] > stdv).all():
                vs2m=0
            if (win.iat[y,col] < stdv).all():
                vs2p=0
            
        print(win)   
        print("vs2p: " + str(vs2p) + " vs2m: " + str(vs2m))
        print("x pass # %d : ",x)
        
        if(vs2p >= 2) or (vs2m >= 2):
            for z in range(0,len(win),1):
                v.append([win.iat[z,col],x+z])
        win = data.loc[x+1:x+3]
    #find 3 sigma violations
    for x in range(1,len(data),1):
        if(data.iat[x,col] > sigma3plus).all():
            v.append(data.iat[x,col])
        if(data.iat[x,col] < sigma3min).all():
            v.append(data.iat[x,col])
    print(v)
    return pandas.DataFrame(v)


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
        stdv = df.std()
        #stdv_json = stdv.to_json(orient = 'values')
        mean = df.mean()
        #mean_json = mean.to_json(oreint = 'values')
        df_json = df.to_json(orient = 'values')
        print(df_json)
        df_violations = srccalculate(df,0)
        df_v_json = df_violations.to_json(orient = 'values')
       # print(csv_file.read().decode("utf-8"))
        #file_data = csv_file.read().decode("utf-8")	
        #print(file_data.split("\n"))
        return render(request, "graph/csv_upload.html", {'df' : df_json, 'dfv' : df_v_json, 'stdv' : stdv, 'mean' : mean})
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
        df_json = (pandas.DataFrame()).to_json(orient = 'values')
    
    return HttpResponseRedirect(reverse("graph:csv_upload"))