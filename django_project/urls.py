from django.urls import path, include

urlpatterns = [
    path("api/contract", include("contract.urls")),
]
