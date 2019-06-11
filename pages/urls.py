from django.urls import path

from .views import HomePageView, TreePageView, FamilyPageView, person_add_view, edge_add_view, XPageView, exportCSV, exportEdges
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('tree/', TreePageView.as_view(), name='tree'),
    path('import/', TreePageView.importPersons, name='import'),
    path('addPerson/', person_add_view, name='addPerson'),
    path('addX/', XPageView.as_view(), name='addX'),
    path('addRelation/', edge_add_view, name='addRelation'),
    url(r'^upload/csv/$', views.upload_csv, name='upload_csv'),
    url(r'^upload/edges/$', views.upload_edges, name='upload_edges'),
    path('edges/', TreePageView.edges, name='edges'),
    path('edgesX/', HomePageView.edges, name='edgesX'),
    url(r'^getNames/$', HomePageView.getNames, name='getNames'),
    url(r'^ajax/new_coordinates/$', views.person_new_coordinates, name='person_new_coordiates'),
    # path('family/', FamilyPageView.as_view(), name='family'),
    url(r'^family/(?P<pk>\d+)/$', FamilyPageView.as_view(), name='memberDetail'),
    url(r'^clan/(?P<family_id>\d+)/$', HomePageView.as_view(), name='clan'),
    url(r'^clanEdit/(?P<family_id>\d+)/$', TreePageView.as_view(), name='clanEdit'),
    path('exportPersons/', views.exportCSV, name='exportCSV'),
    path('exportEdges/', views.exportEdges, name='exportEdges'),
]





