# please install python if it is not present in the system
from setuptools import setup

setup(
 name='django-shopify-lib',
 version='1.0.0',
 packages=['installation'],
 license = 'MIT',
 description = 'Boiler plate code for shopify app installation and other utilities',
 author = 'Sankalp Jonna',
 author_email = 'sankalpjonna@gmail.com',
 keywords = ['shopify', 'django', 'app install'],
 long_description_content_type="text/markdown",
 url="https://github.com/sankalpjonn/django-shopify-lib",
 include_package_data=True,
 install_requires=['Django', 'djangorestframework']
)
