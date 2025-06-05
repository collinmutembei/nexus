from django_pyoidc import get_user_by_email
from django_pyoidc.utils import extract_claim_from_tokens
from .models import Customer


def create_customer(user, phone_number):
    customer, _ = Customer.objects.get_or_create(email=user.email)
    customer.first_name = user.first_name
    customer.last_name = user.last_name
    customer.phone = phone_number
    customer.save()


def get_user(client, tokens):
    user = get_user_by_email(tokens)
    username = extract_claim_from_tokens("preferred_username", tokens)
    phone_number = extract_claim_from_tokens("phone_number", tokens)
    first_name = extract_claim_from_tokens("given_name", tokens)
    last_name = extract_claim_from_tokens("family_name", tokens)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    if username == "admin":
        user.is_staff = user.is_superuser = True
        user.save()
    if phone_number:
        create_customer(user, phone_number)
    return user
