from django.urls import path
from .views import home, contact, about, ServiceListView, TechnologyListView

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('services/', ServiceListView.as_view(), name='services'),
    path('technologies/', TechnologyListView.as_view(), name='technologies'),
]