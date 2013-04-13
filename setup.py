from distutils.core import setup

from upload_avatar import VERSION

packages = [
    'upload_avatar',
]

package_data = {
    'upload_avatar': [
        'static/imgareaselect/*.js',
        'static/imgareaselect/css/*',
        'templates/upload_avatar/upload_avatar.html',
    ]
}

setup(
    name='django-upload-avatar',
    version = VERSION,
    license = 'BSD',
    description = 'A Django APP for Upload avatars',
    long_description = open('README.txt').read(),
    author = 'Wang Chao',
    author_email = 'yueyoum@gmail.com',
    url = 'https://github.com/yueyoum/django-upload-avatar',
    keywords = 'django, avatar',
    packages = packages,
    package_data = package_data,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Internet',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)

