from django.conf.urls import include, url
from django.contrib import admin
import beertemp.views


urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^report/', beertemp.views.report),
    url(r'^templog/', beertemp.views.templog),
    url(r'^tempcsv/', beertemp.views.tempcsv),
    url(r'^tempjs/', beertemp.views.tempjs),
    url(r'^humidcsv/', beertemp.views.humidcsv),
    url(r'^humidjs/', beertemp.views.humidjs),
    url(r'^tempgraph/', beertemp.views.tempgraph),
    url(r'^tempstock/', beertemp.views.tempstock),

    url(r'^dostuff/', beertemp.views.dostuff),

]
