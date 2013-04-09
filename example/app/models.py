from django.db import models


from upload_avatar.signals import avatar_crop_done

class User(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_info')
    avatar_name = models.CharField(max_length=128)


def save_avatar_in_db(sender, uid, avatar_name, **kwargs):
    if User.objects.filter(user_id=uid).exists():
        User.objects.filter(user_id=uid).update(avatar_name=avatar_name)
    else:
        User.objects.create(user_id=uid, avatar_name=avatar_name)
        
    print 'xxx save done...'
    
avatar_crop_done.connect(save_avatar_in_db)
