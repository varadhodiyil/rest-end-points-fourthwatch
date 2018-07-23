from django.conf.urls import url
from fourthwatch.loc import views

urlpatterns = [
	url(r'$', views.InitiateLOC.as_view(), name="initiate_loc"),
]