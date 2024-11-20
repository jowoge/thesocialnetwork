from django.db import models
from django.contrib.auth.models import User

# I wrote this code
# user details model
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    pfp = models.ImageField(upload_to='profile_image', null=True, blank=True)

    def __str__(self):
        return self.user.username

# posts model
class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    text = models.CharField(max_length=10000)
    # stores the image if there is any
    image = models.ImageField(upload_to='post_image', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
# following/follower model
class Followers(models.Model):
    user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    
    def __str__(self):
        return u'user: %s, follower: %s' % (self.user.username, self.follower.username)

# chatrooms model
class Chatroom(models.Model):
    chatroom = models.CharField(max_length=255, unique=True, blank=False)
    user = models.ManyToManyField(User, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chatroom

# chatroom messages    
class ChatroomMessages(models.Model):
    id = models.AutoField(primary_key=True)
    chatroom = models.ForeignKey(Chatroom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
# end of code I wrote