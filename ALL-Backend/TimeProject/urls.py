
from django.urls import path, include

urlpatterns = [
    path('wx_mini/', include("app1.urls")),
]
