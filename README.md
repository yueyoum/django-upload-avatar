# Django-Upload-Avatar

A django app for upload avatars

You can find a showcase at [youtube][1] or [youku][2]


## Install

    pip install django-upload-avatar
    
or clone git repo

    git clone https://github.com/yueyoum/django-upload-avatar.git
    
    
## Usage

It's better that you study the `example` django project first.

#### add `upload_avatar` in your `INSTALLED_APPS`

#### add `url(r'', include('upload_avatar.urls'))` in your project's `urls.py`

#### Necessary settings

###### UPLOAD_AVATAR_UPLOAD_ROOT

where to store the uploaded images.  **Absolute path**.

###### UPLOAD_AVATAR_AVATAR_ROOT

where to store the cropped avatars.  **Absolute path**.

###### UPLOAD_AVATAR_URL_PREFIX_ORIGINAL

URL prefix for the original uploaded image, `<img src="" />` display the uploaded image
for select area and crop. e.g. `uploadedimage/`.

###### UPLOAD_AVATAR_URL_PREFIX_CROPPED

URL prefix for the real avatars. For display avatars in web page


#### In you app

###### models.py

The simplest demo as the `example/app/models.py`

```python
from upload_avatar.signals import avatar_crop_done
from upload_avatar.models import UploadAvatarMixIn

class User(models.Model, UploadAvatarMixIn):
    user = models.ForeignKey('auth.User', related_name='user_info')
    avatar_name = models.CharField(max_length=128)
    
    def get_uid(self):
        return self.user.id
    
    def get_avatar_name(self, size):
        return UploadAvatarMixIn.build_avatar_name(self, self.avatar_name, size)


def save_avatar_in_db(sender, uid, avatar_name, **kwargs):
    if User.objects.filter(user_id=uid).exists():
        User.objects.filter(user_id=uid).update(avatar_name=avatar_name)
    else:
        User.objects.create(user_id=uid, avatar_name=avatar_name)
        
avatar_crop_done.connect(save_avatar_in_db)
```

your user models MUST define a field that store the avatar name,
and inherit from `UploadAvatarMixIn` and define `get_uid`,
`get_avatar_name` methods.

Because `upload_avatar` app does not know how to get `uid` and `avatat_name`

Also, you should define a function which like `save_avatar_in_db` in the example.
and make `avatar_crop_done` signal connected with this function.

#### views.py

In the upload avatar web page, you should pass the uploadavatar_context to template.

demo:

```python
from upload_avatar import get_uploadavatar_context

@login_required
def upload(request):
    return render_to_response(
        'upload.html',
        get_uploadavatar_context(),
        context_instance = RequestContext(request)
    )
```

#### templates

In you `upload.html` template, Just simply do this:

```python
{% include "upload_avatar/upload_avatar.html" %}
```

#### jQuery.js

`upload_avatar` app needs jQuery, So ensure your app/site contains jquery

Details see the `example` django project


[1]: (http://www.youtube.com/watch?v=570yBlCfm5g)
[2]: (http://v.youku.com/v_show/id_XNTQyNDA0OTQ4.html)