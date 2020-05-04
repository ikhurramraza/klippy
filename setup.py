from setuptools import setup, find_packages

from app.version import VERSION

with open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()


setup(
    name='klippy',
    author='Khurram Raza',
    description="A command line utility that acts like a cloud clipboard.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email="ikhurramraza@gmail.com",
    url='https://github.com/ikhurramraza/klippy',
    keywords='cloud clipboard',
    license='MIT',
    classifiers=['License :: OSI Approved :: MIT License'],
    version=VERSION,
    packages=find_packages(exclude=["tests.*", "tests"]),
    scripts=['cli.py'],
    include_package_data=True,
    python_requires='>=3.0, <4',
    install_requires=[
        'click',
        'redis',
    ],
    entry_points='''
        [console_scripts]
        klippy=cli:cli
    ''',
)
