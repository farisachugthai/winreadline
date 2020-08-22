# -*- coding: utf-8 -*-
# Imports: {{{
import codecs
import glob
import logging
import os
import sys
from platform import system

logging.basicConfig()
logger = logging.getLogger(name=__name__)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

    find_packages = None
else:
    from setuptools import find_packages

try:
    import sphinx
except ImportError:
    cmd_class = {}
else:
    from sphinx.setup_command import BuildDoc

    cmd_class = {"build_sphinx": BuildDoc}

if find_packages is not None:
    packages = find_packages()
else:
    packages=["src/winreadline"]

# for distutils setuptools compatabilit.
# TODO: add zip_safe=False
# }}}

# Metadata: {{{
# Name of the package for release purposes.  This is the name which labels
# the tarballs and RPMs made by distutils, so it's best to lowercase it.
name = "pyreadline"

version = "2.1"

description = "A python implmementation of GNU readline."

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(ROOT_PATH, "", "README.rst")

with codecs.open(README, encoding="utf-8") as f:
    long_description = "\n" + f.read()


keywords = ["readline", "windows", "pyreadline"]
platforms = ["Windows XP/2000/NT", "Windows 95/98/ME", "Windows 10"]
# url = "https://github.com/pyreadline/pyreadline"
# download_url = "https://pypi.python.org/pypi/pyreadline"

license = "BSD"

authors = {
    # "Jorgen": ("Jorgen Stenarson", "jorgen.stenarson@kroywen.se"),
    # "Gary": ("Gary Bishop", ""),
    # "Jack": ("Jack Trainor", ""),
}


setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
        long_description_content_type="text/restructuredtext",
        # python_requires=REQUIRES_PYTHON,
    # author=authors["Jorgen"][0],
    # author_email=authors["Jorgen"][1],
    # maintainer=authors["Jorgen"][0],
    # maintainer_email=authors["Jorgen"][1],
    src_root="src/winreadline",
    license=license,
    # where did we define classifiers?
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python",
        # "Programming Language :: Python :: 2",
        # "Programming Language :: Python :: 2.6",
        # "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    # url=url,
    # check that this exists in setuptools
    # download_url=download_url,
    platforms=platforms,
    keywords=keywords,
    packages=packages,
    py_modules=["readline"],
    data_files=[("docs", glob.glob("docs/*")),],
    cmdclass=cmd_class,
    python_requires=">=2.6.0",
    requires=["setuptools", "pywin32", "wheel"],
    # whats the difference between requires, install_requires, setup_requires again?
    # i dont even understand what error this raised but let's leave this
    # commented out
    # setup_requires=["pkg_resources", "pipenv"],
    # They actually really don't but hey
    # install_requires=REQUIRED,
    tests_require=["pytest"],
        test_suite="test",
        include_package_data=True,
    extras_require={"docs": ["sphinx"], "test": ["pytest"]},
        package_data={
            # If any package contains *.txt or *.rst files, include them:
            "": ["*.txt", "*.rst"],
        },
        # # $ setup.py publish support.
        # cmdclass={"upload": UploadCommand},
        # # project home page, if any
        # project_urls={
        #     "Bug Tracker": "https://www.github.com/farisachugthai/dynamic_ipython/issues",
        #     "Documentation": "https://farisachugthai.github.io/dynamic_ipython",
        #     "Source Code": "https://www.github.com/farisachugthai/dynamic_ipython",
        # }
)

# Vim: set fdm=marker:
