from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
    path('destination/<tripid>',views.destination),
    path('add',views.add),
    path('join/<tripid>',views.join),
    path('cancel/<tripid>',views.cancel),
    path('delete/<tripid>',views.delete)
]
