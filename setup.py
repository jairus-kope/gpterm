from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gpterm",
    version="0.2.8",
    author="Jairus",
    author_email="jairus.kope@gmail.com",
    description="A Terminal emulation to interact with OpenAI's GPT models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jairus-kope/gpterm",
    packages=find_packages(),
    install_requires=[
        'openai>=0.26.4',
        'rich>=13.3.1',
        'pyyaml>=6.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: MacOS :: MacOS X',
    ],
    python_requires='>=3.9.6',
    entry_points={
        "console_scripts": [
            "gpterm = gpterm.gpterm:gpterm_main"
        ]
    },
)
