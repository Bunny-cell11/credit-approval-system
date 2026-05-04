import pandas as pd
from celery import shared_task
from .models import Customer, Loan


@shared_task
def load_initial_data():

    customers = pd.read_excel("customer_data.xlsx")
    loans = pd.read_excel("loan_data.xlsx")

    for _, row in customers.iterrows():
        Customer.objects.get_or_create(
            phone_number=row["phone_number"],
            defaults={
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "age": 30,
                "monthly_income": row["monthly_salary"],
                "approved_limit": row["approved_limit"],
                "current_debt": row["current_debt"]
            }
        )

