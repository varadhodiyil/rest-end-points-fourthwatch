from django.conf.urls import url
from fourthwatch.auth_core import views

urlpatterns = [
	url(r'^register/bank$', views.BankRegistration.as_view(), name="register_bank"),
	url(r'^register/bank_employee$', views.BankEmployeeRegistration.as_view(), name="register_bank_employee"),
	url(r'^register/customer$', views.UserRegistration.as_view(), name="register_customer"),
	url(r'^login/$', views.UserLogin.as_view(), name="login"),
	url(r'^profile/$', views.Profile.as_view(), name="profile"),
	
	# url(r'^request_password/', views.RequestForgotPassword.as_view()),
	# url(r'^forgot_password/', views.ForgotPassword.as_view()),
	# url(r'^logout/', views.Logout.as_view()),
]