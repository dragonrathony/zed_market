from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
# from .models import CustomUser as User
from pprint import pprint


class CategoryManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_category(self, **data):
        """
        Create and save a User with the given email and password.
        """
        category = self.model(**data)
        category.save()
        return category

    def update_category(self, pk, data):
        pprint(data)
        self.model.objects.filter(pk=pk).update(**data)

