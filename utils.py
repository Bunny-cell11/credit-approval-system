import math


def calculate_approved_limit(monthly_income):
    limit = 36 * monthly_income
    return round(limit / 100000) * 100000


def calculate_emi(principal, annual_rate, tenure):
    monthly_rate = annual_rate / (12 * 100)

    if monthly_rate == 0:
        return principal / tenure

    emi = principal * monthly_rate * (1 + monthly_rate) ** tenure / \
        ((1 + monthly_rate) ** tenure - 1)

    return round(emi, 2)

