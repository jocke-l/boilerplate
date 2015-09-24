from setuptools import setup, find_packages


setup(
    name='{{ name }}',
    version='{{ version }}',
    description='{{ description }}',
    url='{{ url }}',
    author='{{ author }}',
    author_email='{{ author_email }}',
    license='{{ license }}',
    packages=find_packages(),
)
