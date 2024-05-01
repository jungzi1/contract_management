from rest_framework import serializers

# from contract.models import Contract


# class ContractSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contract
#         fields = [
#             "id",
#             "title",
#             "is"
#         ]


# class ContractCreateSerializer(serializers.ModelSerializer):
#     manager = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = Contract
#         fields = [
#             "id",
#             "title",
#             "manager",
#             "is_reviewed",
#         ]
#         extra_kwargs = {
#             "id": {"read_only": True},
#             "is_reviewed": {"read_only": True},
#         }


# class ContractUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contract
#         fields = [
#             "id",
#             "title",
#             "is_legal_team_confirmed",
#             "legal_team_manager",
#             "is_finance_team_confirmed",
#             "finance_team_manager",
#             "is_security_team_confirmed",
#             "security_team_manager",
#             "is_reviewed",
#         ]
#         extra_kwargs = {
#             "id": {"read_only": True},
#             "is_reviewed": {"read_only": True},
#         }
