import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='betabernsum',
    version='0.1.2',
    author='Anthony Aylward',
    author_email='aaylward@eng.ucsd.edu',
    description='Sums of beta-bernoulli random variables',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/anthony-aylward/betabernsum.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['accelasc', 'scipy']
)
