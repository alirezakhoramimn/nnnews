from django.db import models
from django.contrib.auth.models import User
# for image
from PIL import Image
# Create your models here.

# adding the image to our profile


class Profile(models.Model):
    # cascade : if the user is deleted delete the profile and image as well
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #  if you attention there is a new dir names profile_pics and the picturs are all there
    # as you realize that is really not a good dir because of the messiness
    #   # therefor we need to go to settings.py and give the midia root a root
    bio = models.CharField(default='بیو',max_length=512, null=False,blank=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=False, blank=False)

    
    # let's edit the image size to have less hajm
    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        # let's this image is more than 300 pixels

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


    #  if you attention there is a new dir names profile_pics and the picturs are all there
    # as you realize that is really not a good dir because of the messiness
    #   # therefor we need to go to settings.py and give the midia root a root
'''
    def __str__(self):
        return f'{self.user.username} Profile'

'''
'''
we use user.profile.image.url to find the url (dir) of the image 
this will help us in html to find and show whatever the fuck we are facing in.
'''