from django.urls import path
from .views import RegisterView, CheckEligibilityView, CreateLoanView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("check-eligibility/", CheckEligibilityView.as_view()),
    path("create-loan/", CreateLoanView.as_view()),
]

