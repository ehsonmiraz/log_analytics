from rest_framework.routers import DefaultRouter
from .views import LogIngest
from django.urls import path
# router = DefaultRouter()
# router.register(r'create', LogIngest, basename='log_ingest')
urlpatterns = [
    # Add any additional paths here
    path('create/', LogIngest.as_view(), name="create"),
]
# urlpatterns = router.urls