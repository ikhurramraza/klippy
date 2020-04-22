from setuptools import setup, find_packages

from app.version import VERSION

setup(
    name='klippy',
    author='Khurram Raza',
    description="A command line utility that acts like a cloud clipboard.",
    author_email="ikhurramraza@gmail.com",
    url='https://github.com/ikhurramraza/klippy',
    keywords='cloud clipboard',
    license='MIT',
    classifiers=['License :: OSI Approved :: MIT License'],
    version=VERSION,
    packages=find_packages(),
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
