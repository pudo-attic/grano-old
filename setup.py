from setuptools import setup, find_packages

setup(
    name='grano',
    version='0.1',
    description="SNA (social network analysis) web platform",
    long_description='',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
    keywords='sql graph sna networks journalism ddj',
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    url='http://okfn.org',
    license='AGPLv3',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'sqlalchemy==0.7.4',
        'Flask==0.8',
        'Flask-Script==0.3.1',
        'flask-sqlalchemy==0.15',
        'colander==0.9.4',
        'Unidecode==0.04.9',
        'sqlalchemy-migrate==0.7.2',
        'python-dateutil==2.0',
        'flask-login==0.1',
        'formencode==1.2.4'
    ],
    tests_require=[],
    entry_points=\
    """ """,
)
