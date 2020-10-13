from setuptools import setup, find_packages


setup(
    name='dash_router',
    version='0.2.1',
    description='A simple router for multi page Dash applications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mercy University Hosptial',
    author_email='jharrington@muh.ie',
    url='https://github.com/mercyuniversityhospital/dash_router',
    license='BSD',
    packages=find_packages(exclude=('tests',)),
)