import setuptools

with open('./README.md', 'r') as readme_file:
    readme = readme_file.read()

with open('./tools/cl/convince/install_requirements.txt') as install_requirements:
    install_requires = [line.strip() for line in install_requirements.readlines()]

setuptools.setup(
    name='convince',
    version='0.0.1',
    author='The Project Contributors',
    description='Better instruction following for large language models',
    license='Apache Software License',
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    url='https://github.com/compatibl/convince',
    project_urls={
        'Source Code': 'https://github.com/compatibl/convince',
    },
    packages=setuptools.find_namespace_packages(
        where='.',
        include=['cl.convince', 'cl.convince.*'],
        exclude=['tests', 'tests.*']
    ),
    package_dir={'': '.'},
    classifiers=[
        # Alpha - will attempt to avoid breaking changes but they remain possible
        'Development Status :: 3 - Alpha',

        # Audience and topic
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',

        # License
        'License :: OSI Approved :: Apache Software License',

        # Runs on Python 3.10 and later releases
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',

        # Operating system
        'Operating System :: OS Independent',
    ],
)
