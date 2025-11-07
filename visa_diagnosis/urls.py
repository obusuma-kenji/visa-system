from django.urls import path
from . import views

app_name = 'visa_diagnosis'

urlpatterns = [
    path('', views.index, name='index'),
    path('visa-list/', views.visa_list, name='visa_list'),
    path('diagnose/', views.diagnose, name='diagnose'),
    path('diagnosis-form/', views.diagnosis_form, name='diagnosis_form'),
    path('submit-diagnosis/', views.submit_diagnosis, name='submit_diagnosis'),
]
