
from django.urls import path, include


app_name='parceiros'
urlpatterns = [
    path('laudos-psicologicos/', include('laudoPsicologico.urls')),

    ]