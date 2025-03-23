from django.urls import path
from . import views

app_name = 'credit_score'

urlpatterns = [
    path('', views.credit_score_view, name='credit_score'),
] 