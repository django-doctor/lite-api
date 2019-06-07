from django.urls import path

from static.denial_reasons import views

app_name = 'denial_reasons'

urlpatterns = [
    path('', views.DenialReasonsList.as_view(), name='denial_reasons')
]