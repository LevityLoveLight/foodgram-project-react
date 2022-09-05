from django.urls import include, path
from rest_framework import routers


v1_router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    #path('', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),
]