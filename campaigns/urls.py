from django.urls import path
from . import views

app_name = 'campaigns'
urlpatterns = [
	path('', views.index, name ='index'),
	path('<int:campaign_id>/', views.detail, name ='detail'),
	path('<int:campaign_id>/results/', views.results, name ='results'),
	path('<int:campaign_id>/vote/', views.vote, name ='vote'),
]
