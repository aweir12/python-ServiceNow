import setuptools
import versioneer

with open("README.md", "r") as rm:
    long_description = rm.read().split("\n")[1]

setuptools.setup(
    name="servicenow",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Austin Weir",
    author_email="noreply@noreply.com",
    description=long_description,
    url="https://github.com/aweir12/python-ServiceNow",
    packages=setuptools.find_packages(),
    package_data={'': ['*.csv', '*.yml', '*.html']}
)