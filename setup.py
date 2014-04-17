from setuptools import setup, find_packages

setup(
    name = "pyrannosaurus",
    version = "0.0.1",
    description = "Salesforce Development Tools",
    author = "KC Shafer",
    author_email = "kclshafer@gmail.com",
    url = "https://github.com/kcshafer/pyrannosaurus/",
    keywords = ["salesforce"],
    install_requires = [
        "suds==0.4"
    ],
    packages = find_packages(),
    long_description = """\
    Salesforce Development Tools
    ----------------------------
    """
)
