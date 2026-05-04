from datetime import datetime
from .utils import calculate_emi


def calculate_credit_score(customer):

    loans = customer.loans.all()

    if customer.current_debt > customer.approved_limit:
        return 0

    score = 0
    total_loans = loans.count()

    if total_loans == 0:
        return 50

    total_emis = sum([loan.tenure for loan in loans])
    paid_on_time = sum([loan.emis_paid_on_time for loan in loans])

    if total_emis > 0:
        score += (paid_on_time / total_emis) * 40

    if total_loans <= 2:
        score += 20
    elif total_loans <= 5:
        score += 10

    current_year = datetime.now().year
    if loans.filter(start_date__year=current_year).exists():
        score += 20

    total_volume = sum([loan.loan_amount for loan in loans])
    if total_volume < customer.approved_limit:
        score += 20

    return min(100, int(score))


def check_eligibility(customer, loan_amount, interest_rate, tenure):

    credit_score = calculate_credit_score(customer)

    emi = calculate_emi(loan_amount, interest_rate, tenure)
    current_emis = sum(
        [loan.monthly_installment for loan in customer.loans.filter(is_active=True)]
    )

    if current_emis + emi > 0.5 * customer.monthly_income:
        return False, interest_rate, emi, "EMI exceeds 50% salary"

    corrected_rate = interest_rate

    if credit_score > 50:
        approved = True
    elif 30 < credit_score <= 50:
        corrected_rate = max(interest_rate, 12)
        approved = interest_rate >= 12
    elif 10 < credit_score <= 30:
        corrected_rate = max(interest_rate, 16)
        approved = interest_rate >= 16
    else:
        return False, interest_rate, emi, "Low credit score"

    emi = calculate_emi(loan_amount, corrected_rate, tenure)

    return approved, corrected_rate, emi, None

