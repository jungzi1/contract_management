from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.request import Request

from contract.models import Contract
from contract.serializers import (
    ContractSerializer, ContractCreateSerializer, ContractUpdateSerializer
)

class ContractListView(ListModelMixin, GenericAPIView):
    queryset = Contract.objects.order_by("-id")
    serializer_class = ContractSerializer

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ContractCreateView(CreateModelMixin, GenericAPIView):
    queryset = Contract.objects.order_by("-id")
    serializer_class = ContractCreateSerializer

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ContractUpdateView(UpdateModelMixin, GenericAPIView):
    queryset = Contract.objects.order_by("-id")
    serializer_class = ContractUpdateSerializer

    def patch(self, request: Request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)
