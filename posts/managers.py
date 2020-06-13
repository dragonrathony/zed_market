from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from pprint import pprint


class PostManager():
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_post(self, **data):

        post_data = self.model(**data)
        print(post_data, '-----------------------------------------------')
        post_data.save()
        return post_data

    def update_post(self, pk, data):
        pprint(data)
        self.model.objects.filter(pk=pk).update(**data)

    def list_post(self, category):
        return self.model.objects.filter(category=category)
