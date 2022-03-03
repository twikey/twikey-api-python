from setuptools import setup, find_packages
import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_long_description():
    return open(os.path.join(ROOT_DIR, "README.md")).read()


setup(
    name="twikey-api-python",
    version="v0.1.3",
    description="Python interface with the Twikey api",
    author="Twikey",
    author_email="support@twikey.com",
    url="https://github.com/twikey/twikey-api-python",
    license="MIT",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords="twikey api payments",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"',
        'requests[security] >= 2.20; python_version < "3.0"',
    ],
    python_requires=">=3.6",
    project_urls={
        "Bug Tracker": "https://github.com/twikey/twikey-api-python/issues",
        "Source Code": "https://github.com/twikey/twikey-api-python",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
