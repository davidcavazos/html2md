import setuptools

with open("README.md") as f:
  long_description = f.read()

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setuptools.setup(
    name="html2md",
    version="0.1.1",
    author="David Cavazos",
    author_email="dcavazosw@gmail.com",
    description="HTML to Markdown converter.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidcavazos/html2md",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'html2md = html2md.__main__:main'
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
    ],
)
