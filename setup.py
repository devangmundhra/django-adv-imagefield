from distutils.core import setup

setup(
  name = 'django-adv-imagefield',
  packages = ['django-adv-imagefield'],
  version = '0.1',
  description = 'Advanced ImageField for Django that provides widget to search Flickr and Google Images',
  author = 'Devang Mundhra',
  author_email = 'devangmundhra@gmail.com',
  url = 'https://github.com/devangmundhra/django-adv-imagefield',
  license='MIT',
  download_url = 'https://github.com/devangmundhra/django-adv-imagefield/0.1',
  keywords = ['django', 'imagefield', 'media', 'flickr', 'google-image-search',],
  install_requires=[
        'django>=1.3',
        ],
  classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)