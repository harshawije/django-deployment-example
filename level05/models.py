from django.db import models
from django.contrib.auth.models import User

# Extended class to add more fields to User.


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional information

    portfolio_site =  models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username # default attribute of user