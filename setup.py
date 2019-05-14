from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='dash_router',
    version='0.1.0',
    description='A simple router for multi page Dash applications.',
    long_description=readme,
    long_description_content_type='text/markdown'
    author='Mercy University Hosptial',
    author_email='jharrington@muh.ie',
    url='https://github.com/mercyuniversityhospital/dash_reporting',
    license=license,
    packages=find_packages(exclude=('tests'))
)