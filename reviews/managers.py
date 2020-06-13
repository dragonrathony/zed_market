from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from pprint import pprint


class ReviewsManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_review(self, **data):
        """
        Create and save a User with the given email and password.
        """
        email = data["buyer_email"]
        email = self.normalize_email(email)
        review = self.model(**data)
        review.save()
        return review


    def list_review(self, ad_id):
        return self.model.objects.filter(ad_id=ad_id)
