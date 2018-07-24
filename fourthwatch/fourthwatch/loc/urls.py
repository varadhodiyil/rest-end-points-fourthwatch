from django.conf.urls import url
from fourthwatch.loc import views

urlpatterns = [
	url(r'^loc/(?P<id>[0-9]+)/$', views.LOCAPI.as_view(), name="loc"),
	url(r'^loc/$', views.InitiateLOC.as_view(), name="initiate_loc"),
	url(r'^loc/approve/$', views.ApproveAPI.as_view(), name="approve_loc"),
	url(r'^loc/reject/$', views.RejectAPI.as_view(), name="reject_loc"),
	url(r'^loc/ship_product/$', views.ShipProductAPI.as_view(), name="ship_product"),
	url(r'^loc/receive_product/$', views.ReceiveProductAPI.as_view(), name="ship_product"),
	url(r'^loc/ready_payment/$', views.ReadyForPaymentAPI.as_view(), name="ready_product"),
	url(r'^loc/close/$', views.CloseAPI.as_view(), name="close"),
	url(r'^customers$', views.Customers.as_view(), name="customers"),
]
