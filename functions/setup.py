from setuptools import setup, find_packages

setup(
    name='my-fastapi-project',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic',
        'python-dotenv',
        'requests',
        'firebase-functions'
    ]
)
