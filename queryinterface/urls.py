from django.urls import path
from .views import LogSearch

urlpatterns = [
    path('logs/', LogSearch.as_view(), name='log-search'),
]

# urlpatterns = router.urls