from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .models import Customer, Loan
from .utils import calculate_approved_limit
from .services import check_eligibility


class RegisterView(APIView):

    def post(self, request):

        approved_limit = calculate_approved_limit(
            request.data["monthly_income"]
        )

        customer = Customer.objects.create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            age=request.data["age"],
            phone_number=request.data["phone_number"],
            monthly_income=request.data["monthly_income"],
            approved_limit=approved_limit
        )

        return Response({
            "customer_id": customer.id,
            "name": f"{customer.first_name} {customer.last_name}",
            "age": customer.age,
            "monthly_income": customer.monthly_income,
            "approved_limit": customer.approved_limit,
            "phone_number": customer.phone_number
        }, status=status.HTTP_201_CREATED)


class CheckEligibilityView(APIView):

    def post(self, request):

        customer = Customer.objects.get(id=request.data["customer_id"])

        approved, corrected_rate, emi, message = check_eligibility(
            customer,
            request.data["loan_amount"],
            request.data["interest_rate"],
            request.data["tenure"]
        )

        return Response({
            "customer_id": customer.id,
            "approval": approved,
            "interest_rate": request.data["interest_rate"],
            "corrected_interest_rate": corrected_rate,
            "tenure": request.data["tenure"],
            "monthly_installment": emi
        })


class CreateLoanView(APIView):

    def post(self, request):

        customer = Customer.objects.get(id=request.data["customer_id"])

        approved, corrected_rate, emi, message = check_eligibility(
            customer,
            request.data["loan_amount"],
            request.data["interest_rate"],
            request.data["tenure"]
        )

        if not approved:
            return Response({
                "loan_id": None,
                "customer_id": customer.id,
                "loan_approved": False,
                "message": message,
                "monthly_installment": emi
            })

        end_date = timezone.now().date() + timedelta(days=30 * request.data["tenure"])

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=request.data["loan_amount"],
            tenure=request.data["tenure"],
            interest_rate=corrected_rate,
            monthly_installment=emi,
            end_date=end_date
        )

        return Response({
            "loan_id": loan.id,
            "customer_id": customer.id,
            "loan_approved": True,
            "message": "Loan approved",
            "monthly_installment": emi
        })

