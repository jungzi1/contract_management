from rest_framework import serializers

from contract.models import Contract, ContractReviewDepartment
from account.models import User


class ReviewSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
     )

    class Meta:
        model = ContractReviewDepartment
        fields = ['department', 'manager', 'is_confirm']


class ContractSerializer(serializers.ModelSerializer):
    manager_username = serializers.SerializerMethodField('get_manager')
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Contract
        fields = [
            "id",
            "title",
            "manager_username",
            "reviews"
        ]
        
    def get_manager(self, obj):
        if not obj.manager_id:
            return "담당자 없음"
        manager = User.objects.get(id=obj.manager_id)
        return manager.name       


class ContractCreateSerializer(serializers.ModelSerializer):
    manager = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contract
        fields = [
            "id",
            "title",
            "manager",
            "is_private"
        ]
        extra_kwargs = {
            "id": {"read_only": True}
        }



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
