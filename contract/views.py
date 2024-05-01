import json
from rest_framework.views import APIView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from contract.models import Contract, ContractReviewDepartment
from contract.serializers import (
    ContractSerializer, ContractCreateSerializer
)


class ContractView(APIView):
    def post(self, request):
        """ 계약서 작성 """
        reviews = request.data.pop("reviews")
        serializer = ContractCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            ContractReviewDepartment.objects.bulk_create([
                ContractReviewDepartment(department=review, contract_id=serializer.data["id"]) for review in reviews
            ])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """ 계약 목록 조회 """
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        
        return Response(
            {"data": serializer.data},
            status=status.HTTP_200_OK,
        )
