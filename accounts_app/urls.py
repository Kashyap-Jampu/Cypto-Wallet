from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('register',views.register_view,name="register_view"),
    path('login',views.login_view,name="login_view"),
    path('logout',views.logout_view,name="logout_view"),
    path('add_tx',views.add_transaction,name="add_transaction"),


    ]
