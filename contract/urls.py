from django.urls import path

from contract.views import ContractView

urlpatterns = [
    path('', ContractView.as_view()),
]