from setuptools import setup


setup(
    name='fastapi-cli',
    version='0.1',
    py_modules=['chanshi'],
    install_requires=[
        'Click',
        "alembic==1.4.3"
    ],
    entry_points='''
        [console_scripts]
        fastapi=chanshi.cli:fastapi
    ''',
)