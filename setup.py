import setuptools

with open('./README.md', 'r') as readme_file:
    readme = readme_file.read()

with open('./requirements.txt') as requirements_file:
    requirements = [line.strip() for line in requirements_file.readlines()]

setuptools.setup(
    name='cl-runtime',
    version='2.0.0',
    author='The Project Contributors',
    description='CompatibL Runtime Community Edition',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=setuptools.find_namespace_packages(where='.', include=['cl.runtime*']),
    package_dir={'': '.'},
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: Apache Software License",
        'Operating System :: OS Independent',
    ],
)
