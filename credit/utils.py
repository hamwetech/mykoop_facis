from credit.models import LoanTransaction
from conf.utils import generate_alpanumeric, generate_numeric


def create_loan_transaction(params):
    member = params.get('member')
    loan = params.get('loan')
    credit_manager = params.get('credit_manager')
    amount = params.get('amount')
    transaction_type = params.get('transaction_type')
    created_by = params.get('created_by')
    reference = generate_numeric(8, "45")

    LoanTransaction.objects.create(
        reference=reference,
        loan=loan,
        member=member,
        credit_manager=credit_manager,
        amount=amount,
        transaction_type=transaction_type,
        created_by=created_by
    )

    if transaction_type == "DEBIT":
        amount = -amount
    return amount
