from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view_function, name='my_view'),  # This pattern doesn't need 'myapp/' prefix
    # Add more URL patterns as needed
    path('', views.landing_page, name='landing_page'),
]
