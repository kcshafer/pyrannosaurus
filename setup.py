from setuptools import setup, find_packages

setup(
    name = "pyrannosaurus",
    version = "0.0.0",
    description = "Salesforce Development Tools",
    author = "KC Shafer",
    author_email = "kclshafer@gmail.com",
    url = "https://github.com/kcshafer/pyrannosauruspagoda/",
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
