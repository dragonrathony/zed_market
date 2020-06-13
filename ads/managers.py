from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
# from .models import CustomUser as User
from pprint import pprint


class AdListManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_ad(self, **data):
        """
        Create and save a User with the given email and password.
        """
        email = data["email"]
        email = self.normalize_email(email)
        ad = self.model(**data)
        ad.save()
        return ad

    def update_ad(self, pk, data):
        pprint(data)
        self.model.objects.filter(pk=pk).update(**data)

    def list_ads(self, email):
        return self.model.objects.filter(email=email)
