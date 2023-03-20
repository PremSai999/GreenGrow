def deg(normal,preds):
    d = {}
    for i in normal:
        if (float(normal[i])<float(preds[i])):
            d[i]=str(round(((float(preds[i])-float(normal[i]))/float((preds[i]))*100),2))+"%"
        else:
            d[i]="No Degradation"
    return d
