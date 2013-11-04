import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='arkestra-clinical-trials',
    version='0.1',
    packages=['clinical_trials'],
    include_package_data=True,
    license='BSD License',  # example license
    description='Manage and publish information clinical trials in Arkestra',
    long_description=README,
    url='https://github.com/evildmp/arkestra-clinical-trials',
    author='Daniele Procida',
    author_email='daniele@vurt.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # replace these appropriately if you are using Python 3
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
