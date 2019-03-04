from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.utils import timezone

from datetime import timedelta
import random

from beertemp.models import TemperatureRecord


def report(request):
    response = "Backend - OK!"
    t0 = request.GET.get('t0', None)
    h0 = request.GET.get('h0', None)
    t1 = request.GET.get('t1', None)
    h1 = request.GET.get('h1', None)

    when = timezone.now()
    try:
        t0 = float(t0)
        h0 = float(h0)
        t1 = float(t1)
        h1 = float(h1)
        TemperatureRecord.objects.create(
            t0=t0, h0=h0, t1=t1, h1=h1, time=when
        )
    except Exception as e:
        response = "Backend - ERROR"

    return HttpResponse(response)

def _normalize(v, vmin, vmax):
    return max(min(v, vmax), vmin)

def dostuff(request):
    dt = timezone.now()
    tdelta = timedelta(minutes=5)

    random.seed()
    
    t0 = 20.0
    t1 = 19.0
    h0 = 55.0
    h1 = 56.0
    while dt > timezone.now() - timedelta(days=2):
        print(dt, t0, t1, h0, h1)
        TemperatureRecord.objects.create(t0=t0, h0=h0, t1=t1, h1=h1, time=dt)
        t0 += random.uniform(-1.0, 1.0)
        t1 += random.uniform(-1.0, 1.0)
        h0 += random.uniform(-2.0, 2.0)
        h1 += random.uniform(-2.0, 2.0)
        t0 = _normalize(t0, 10, 30)
        t1 = _normalize(t1, 10, 30)
        h0 = _normalize(h0, 45, 95)
        h1 = _normalize(h1, 45, 95)
        dt = dt - tdelta
    return HttpResponse("Done!")

def templog(request):
    tinstances = TemperatureRecord.objects.all()
    tdata = [str(ti) for ti in tinstances]
    return HttpResponse("<br/>\n".join(tdata))

def tempcsv(request):
    tz = timezone.get_current_timezone()
    tinstances = TemperatureRecord.objects.all().order_by('time')
    csv_headr = "Fecha,Temperatura 0,Temperatura 1"
    csv_templ = "%s,%5.2f,%5.2f"
    tfmt = "%Y/%m/%d %H:%M:%S"
    lines = [csv_templ % (t.time.astimezone(tz).strftime(tfmt), t.t0, t.t1)
        for t in tinstances
    ]
    return HttpResponse(csv_headr + "\n" + "\n".join(lines))

def tempjs(request):
    tz = timezone.get_current_timezone()
    tinstances = TemperatureRecord.objects.all().order_by('time')
    csv_templ = "[%s,%5.2f]"
    t0 = [
        csv_templ % (t.time.astimezone(tz).strftime("%s000"), t.t0)
        for t in tinstances
    ]
    t1 = [
        csv_templ % (t.time.astimezone(tz).strftime("%s000"), t.t1)
        for t in tinstances
    ]
    t0 = "[" + ",\n".join(t0) + "\n]"
    t1 = "[" + ",\n".join(t1) + "\n]"
    response = HttpResponse("[" + t0 + ",\n" + t1 + "\n]", content_type="text/javascript")
    return response

def humidjs(request):
    tz = timezone.get_current_timezone()
    tinstances = TemperatureRecord.objects.all().order_by('time')
    csv_templ = "[%s,%5.2f]"
    t0 = [
        csv_templ % (t.time.astimezone(tz).strftime("%s000"), t.h0)
        for t in tinstances
    ]
    t1 = [
        csv_templ % (t.time.astimezone(tz).strftime("%s000"), t.h1)
        for t in tinstances
    ]
    t0 = "[" + ",\n".join(t0) + "\n]"
    t1 = "[" + ",\n".join(t1) + "\n]"
    response = HttpResponse("[" + t0 + ",\n" + t1 + "\n]", content_type="text/javascript")
    return response

def humidcsv(request):
    tz = timezone.get_current_timezone()
    tinstances = TemperatureRecord.objects.all().order_by('time')
    csv_headr = "Fecha,%Humedad0,%Humedad1"
    csv_templ = "%s,%5.2f,%5.2f"
    tfmt = "%Y/%m/%d %H:%M:%S"
    lines = [csv_templ % (t.time.astimezone(tz).strftime(tfmt), t.h0, t.h1)
        for t in tinstances
    ]
    return HttpResponse(csv_headr + "\n" + "\n".join(lines))

def tempgraph(request):
    context = dict()
    return render_to_response("tempgraph.html", context)

def tempstock(request):
    context = dict()
    return render_to_response("tempstock.html", context)
