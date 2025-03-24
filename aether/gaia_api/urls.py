from django.contrib import admin
from django.urls import path
from rest_api.views import hello_vue, get_gaia_response_rapid, get_gaia_response_vocal

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hello', hello_vue),
    path('api/get_rapid_response/<str:message>/', get_gaia_response_rapid, name='message'),
    path('api/get_vocal_response/<str:message>/', get_gaia_response_vocal, name='message')
]
