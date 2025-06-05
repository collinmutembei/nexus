from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from .models import Customer


class OIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(OIDCAuthenticationBackend, self).create_user(claims)
        if claims.get("preferred_username") == "admin":
            user.is_staff = True
            user.is_superuser = True
            user.save()
        # Create a Customer instance for the new user
        Customer.objects.create(
            first_name=claims.get("given_name", ""),
            last_name=claims.get("family_name", ""),
            email=user.email,
        )
        return user

    def update_user(self, user, claims):
        super(OIDCAuthenticationBackend, self).update_user(user, claims)
        # Update the Customer instance with the latest claims
        customer = Customer.objects.get(email=user.email)
        customer.first_name = claims.get("given_name", customer.first_name)
        customer.last_name = claims.get("family_name", customer.last_name)
        customer.save()
