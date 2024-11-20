import factory
from django.contrib.auth.models import User
from .models import AppUser, Posts

# I wrote this code
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')

class AppUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AppUser

    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    dob = factory.Faker('date_of_birth')
    pfp = factory.django.ImageField(filename='test_image.jpg')

class PostsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Posts

    user = factory.SubFactory(UserFactory)
    text = factory.Faker('text')
    image = factory.django.ImageField(filename='post_image.jpg')
    timestamp = factory.Faker('date_time_this_century')
# end of code I wrote