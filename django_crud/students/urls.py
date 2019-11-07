from django.urls import path
from . import views


urlpatterns = [
    path('', views.studentlist),
    path('studentlist/', views.studentlist),
    path('addstudent/', views.addstudent),
    path('studentadded/', views.studentadded),

]