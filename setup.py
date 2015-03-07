from distutils.core import setup

setup(
  name = 'django-adv-imagefield',
  packages = ['media-field'],
  version = '0.0.2',
  description = 'Advanced ImageField for Django that provides widget to search Flickr and Google Images',
  author = 'Devang Mundhra',
  author_email = 'devangmundhra@gmail.com',
  url = 'https://github.com/devangmundhra/django-adv-imagefield',
  license='MIT',
  download_url = 'https://github.com/devangmundhra/django-adv-imagefield/0.0.2',
  keywords = ['django', 'imagefield', 'media', 'flickr', 'google-image-search',],
  install_requires=[
        'Django>=1.7',
        'Pillow>=2.7.0',
        'BeautifulSoup>=3.2.1',
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