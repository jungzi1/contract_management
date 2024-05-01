import json

from time import sleep

from account.models import User
from rest_framework.test import APITestCase
from contract.models import Contract

# noinspection SpellCheckingInspection
class ContractListViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.일반사용자 = User.objects.create(name="일반사용자", email="normal@toss.co.kr", department="NORMAL")
        cls.재무팀사용자 = User.objects.create(name="재무팀사용자", email="finance@toss.co.kr", department="FINANCE")
        cls.법무팀사용자 = User.objects.create(name="법무팀사용자", email="legal@toss.co.kr", department="LEGAL")
        cls.보안팀사용자 = User.objects.create(name="보안팀사용자", email="security@toss.co.kr", department="SECURITY")
        cls.보안기술팀사용자 = User.objects.create(name="보안기술팀사용자", email="security_tech@toss.co.kr", department="SECURITY_TECH")
        cls.기타사용자 = User.objects.create(name="기타사용자", email="etc@toss.co.kr", department="ETC")
        cls.일반사용자.set_password("일반사용자123@")
        cls.재무팀사용자.set_password("재무팀사용자123@")
        cls.법무팀사용자.set_password("법무팀사용자123@")
        cls.보안팀사용자.set_password("보안팀사용자123@")
        cls.보안기술팀사용자.set_password("보안기술팀사용자123@")
        cls.기타사용자.set_password("기타사용자123@")
        cls.일반사용자.save()
        cls.재무팀사용자.save()
        cls.법무팀사용자.save()
        cls.보안팀사용자.save()
        cls.기타사용자.save()
        cls.보안기술팀사용자.save()

    def test_재무팀_확인이_필요한_공개_계약을_등록한다(self):
        self.client.force_authenticate(self.일반사용자)

        data = {
            "title": "계약 명",
            "is_private": False,
            "reviews": ["FINANCE_TEAM"] 
        }
        # 계약 등록
        res = self.client.post(
            "/api/contract",
            json.dumps(data),
            content_type="application/json",
        )
        
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIsNotNone(data["id"])

        contract = Contract.objects.get(pk=data["id"])
        self.assertEqual(data["id"], contract.id)

        for review in contract.reviews.all():
            self.assertEqual(review.department, "FINANCE_TEAM")

        return contract

    def test_비공개_계약을_등록한다(self):
        self.client.force_authenticate(self.일반사용자)

        data = {
            "title": "계약 명",
            "is_private": False,
            "reviews": ["FINANCE_TEAM"],
            "is_private": True
        }
        # 계약 등록
        res = self.client.post(
            "/api/contract",
            json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIsNotNone(data["id"])

        contract = Contract.objects.get(pk=data["id"])
        self.assertEqual(data["id"], contract.id)
        self.assertTrue(contract.is_private)

        for review in contract.reviews.all():
            self.assertEqual(review.type, "FINANCE_TEAM")

    def test_재무팀_사용자로_비공개_계약을_등록한다(self):
        self.client.force_authenticate(self.일반사용자)

        data = {
            "title": "계약 명",
            "is_private": False,
            "reviews": ["FINANCE_TEAM"],
            "is_private": True
        }
        # 계약 등록
        res = self.client.post(
            "/api/contract",
            json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIsNotNone(data["id"])

        contract = Contract.objects.get(pk=data["id"])
        self.assertEqual(data["id"], contract.id)
        self.assertTrue(contract.is_private)

        for review in contract.review_set.all():
            self.assertEqual(review.type, "FINANCE_TEAM")

    def test_재무팀과_보안기술팀_확인이_필요한_공개_계약을_등록한다(self):
        self.client.force_authenticate(self.일반사용자)

        data = {
            "title": "계약 명",
            "is_private": False,
            "reviews": ["FINANCE_TEAM", "SECURITY_TECH_TEAM"],
            "is_private": True
        }
        # 계약 등록
        res = self.client.post(
            "/api/contract",
            json.dumps(data),
            content_type="application/json",
        )
        data = res.json()

        self.assertIsNotNone(data["id"])
        self.assertEqual(data["title"], "계약 명")

        for review in data["reviews"]:
            self.assertIn(review["type"], ["FINANCE_TEAM", "SECURITY_TECH_TEAM"])

    # def test_계약의_제목을_수정한다(self):
    #     contract = self.test_재무팀_확인이_필요한_공개_계약을_등록한다()

    #     # 생성한 계약을 수정
    #     res = self.client.patch(
    #         path=f"/contract/{contract.id}/",
    #         data={"title": "새로운 계약 명"},
    #         content_type="application/json",
    #     )
    #     data = res.json()
    #     self.assertIsNotNone(data["id"])

    #     contract = Contract.objects.get(pk=data["id"])
    #     self.assertEqual(contract.title, "새로운 계약 명")

    # def test_본인의_담당이_아닌_계약을_수정한다(self):
    #     contract = self.test_재무팀_확인이_필요한_공개_계약을_등록한다()

    #     self.client.force_login(self.기타사용자)

    #     # 생성한 계약을 수정
    #     res = self.client.patch(
    #         path=f"/contract/{contract.id}/",
    #         data={"title": "새로운 계약 명"},
    #         content_type="application/json",
    #     )
    #     self.assertEqual(res.status_code, 403)

    # def test_계약의_재무팀_담당자를_지정한다(self):
    #     contract = self.test_재무팀_확인이_필요한_공개_계약을_등록한다()

    #     # 기본 상태를 체크한다.
    #     contract = Contract.objects.get(pk=contract.id)
    #     review = contract.review_set.filter(type="FINANCE_TEAM").first()
    #     self.assertIsNotNone(review)
    #     self.assertIsNone(review.manager)

    #     # 생성한 계약의 재무팀 담당자를 수정한다.
    #     res = self.client.patch(
    #         path=f"/contract/{contract.id}/reviews/FINANCE_TEAM/",
    #         data={"manager": self.재무팀사용자.id},
    #         content_type="application/json",
    #     )
    #     self.assertIs(res.status_code, 200)

    #     contract = Contract.objects.get(pk=contract.id)
    #     review = contract.review_set.filter(type="FINANCE_TEAM").first()
    #     self.assertIsNotNone(review)
    #     self.assertIsNotNone(review.manager)
    #     self.assertIs(review.manager.id, self.재무팀사용자.id)

    #     return contract

    # def test_재무팀_사용자로_계약의_재무팀_상태를_수정한다(self):
    #     contract = self.test_계약의_재무팀_담당자를_지정한다()

    #     self.client.force_login(self.재무팀사용자)

    #     # 생성한 계약의 재무팀 담당자를 수정한다.
    #     res = self.client.patch(
    #         path=f"/contract/{contract.id}/reviews/FINANCE_TEAM/",
    #         data={"is_confirmed": True},
    #         content_type="application/json",
    #     )
    #     self.assertIs(res.status_code, 200)

    #     contract = Contract.objects.get(pk=contract.id)
    #     review = contract.review_set.filter(type="FINANCE_TEAM").first()
    #     self.assertIsNotNone(review)
    #     self.assertIsNotNone(review.manager)
    #     self.assertEqual(review.manager, self.재무팀사용자)
    #     self.assertTrue(review.is_confirmed)

    # def test_법무팀_사용자로_계약의_재무팀_상태를_수정한다(self):
    #     contract = self.test_계약의_재무팀_담당자를_지정한다()

    #     self.client.force_login(self.법무팀사용자)

    #     # 생성한 계약의 재무팀 담당자를 수정한다.
    #     res = self.client.patch(
    #         path=f"/contract/{contract.id}/reviews/FINANCE_TEAM/",
    #         data={"is_confirmed": True},
    #         content_type="application/json",
    #     )
    #     self.assertEqual(res.status_code, 403)

    # def test_계약_확인_담당_팀을_수정한다(self):
    #     """
    #     ["FINANCE_TEAM"] -> ["SECURITY_TEAM", "LEGAL_TEAM"]
    #     """
    #     contract = self.test_재무팀_확인이_필요한_공개_계약을_등록한다()

    #     # 생성한 계약을 수정
    #     res = self.client.patch(
    #         path=f"/contract/{contract.id}/",
    #         data={"review_types": ["SECURITY_TEAM", "LEGAL_TEAM"]},
    #         content_type="application/json",
    #     )
    #     data = res.json()
    #     self.assertIsNotNone(data["id"])

    #     contract = Contract.objects.get(pk=data["id"])
    #     for review in contract.review_set.all():
    #         with self.subTest(state="수정", review_type=review):
    #             self.assertIn(review.type, ["SECURITY_TEAM", "LEGAL_TEAM"])

    # def test_내가_만든_공개_계약을_조회한다(self):
    #     for _ in range(20):
    #         self.test_계약의_재무팀_담당자를_지정한다()

    #     sleep(2)
    #     print("=== created ===", flush=True)
    #     sleep(2)

    #     # 생성한 계약을 조회
    #     with self.assertNumQueriesLessThan(7):
    #         res = self.client.get(path="/contract/")

    #     data = res.json()
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(len(data), 20)
    #     for contract_data in data:
    #         self.assertEqual(contract_data["manager_username"], self.일반사용자.username)
    #         for review_data in contract_data["reviews"]:
    #             self.assertEqual(review_data["manager_username"], self.재무팀사용자.username)

    # def test_내가_만든_비공개_계약을_조회한다(self):
    #     for _ in range(20):
    #         self.test_비공개_계약을_등록한다()

    #     # 생성한 계약을 조회
    #     with self.assertNumQueriesLessThan(6):
    #         res = self.client.get(path="/contract/")
    #     data = res.json()
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(len(data), 20)

    # def test_재무팀_사용자가_만든_비공개_계약을_조회한다(self):
    #     self.test_재무팀_사용자로_비공개_계약을_등록한다()

    #     self.client.force_login(self.일반사용자)

    #     # 생성한 계약을 수정
    #     res = self.client.get(path="/contract/")
    #     data = res.json()
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(len(data), 0)

    # def test_재무팀_사용자로_담당_계약을_조회한다(self):
    #     self.test_계약의_재무팀_담당자를_지정한다()
    #     self.test_비공개_계약을_등록한다()
    #     self.test_재무팀_사용자로_비공개_계약을_등록한다()

    #     self.client.force_login(self.재무팀사용자)

    #     # 생성한 계약을 수정
    #     res = self.client.get(path="/contract/")
    #     data = res.json()
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(len(data), 2)
