import setuptools

with open('./README.md', 'r') as readme_file:
    readme = readme_file.read()

# Gather package requirements from all packages in monorepo
package_requirements = []
with open('./tools/cl/runtime/package_requirements.txt') as runtime_package_requirements:
    package_requirements.extend(line.strip() for line in runtime_package_requirements.readlines())
with open('./tools/cl/convince/package_requirements.txt') as convince_package_requirements:
    package_requirements.extend(line.strip() for line in convince_package_requirements.readlines())
with open('./tools/cl/tradeentry/package_requirements.txt') as tradeentry_package_requirements:
    package_requirements.extend(line.strip() for line in tradeentry_package_requirements.readlines())

setuptools.setup(
    name='tradeentry',
    version='0.0.1',
    author='The Project Contributors',
    description='Trade entry from natural language for capital markets using LLMs',
    license='Apache Software License',
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=package_requirements,
    url='https://github.com/compatibl/tradeentry',
    project_urls={
        'Source Code': 'https://github.com/compatibl/tradeentry',
    },
    packages=setuptools.find_namespace_packages(
        where='.',
        include=['cl.tradeentry', 'cl.tradeentry.*'],
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
