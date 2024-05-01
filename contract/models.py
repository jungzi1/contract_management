from django.db import models

from account.models import Department, User

class Contract(models.Model):
    title = models.CharField(verbose_name="제목", max_length=256)
    is_confirmed = models.BooleanField(verbose_name="계약 확인 여부", default=False)
    manager = models.ForeignKey(
        verbose_name="계약 담당자",
        to=User,
        on_delete=models.DO_NOTHING,
    )
    is_private = models.BooleanField(verbose_name="민감 계약 정보 여뷰", default=False)

    class Meta:
        db_table = "contracts"
        verbose_name = "계약"
        verbose_name_plural = "계약 목록"


class ContractReviewDepartment(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="contracts", verbose_name="담당자 부서"
    )
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="reviewers", verbose_name="계약"
    )
    manager = models.ForeignKey(
        User, on_delete=models.PROTECT, 
        related_name="managing_contracts", 
        verbose_name="담당자"
    )
    is_confirm = models.BooleanField(verbose_name="담당자 확인 여부", default=False)

    class Meta:
        db_table = "contract_review_departments"
        verbose_name = "계약 승인"
        verbose_name_plural = "계약 승인 목록"