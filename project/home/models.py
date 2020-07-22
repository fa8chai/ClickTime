from django.db import models
from profile.models import Profile
import uuid


def images_directory_path(instance, filename):
    return '/'.join(['posts', str(instance.post.id), str(uuid.uuid4().hex + '.png')])


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE , related_name='posts')
    text = models.TextField(max_length=1000,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def get_index(self, image):
        images = self.images.all()
        l_image = enumerate(images, 1)
        for index, img in l_image:
            if not image == img:
                continue
            else:
                return index
            
        

    def __str__(self):
        return f"A post by {self.user.username} "

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=images_directory_path)
    created_on = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE , related_name='likes')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("user", "post")
        
    def __str__(self):
        return f" {self.user.username} liked {self.post.user.username} post "



class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} : {self.text}"

