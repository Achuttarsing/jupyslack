# setup.py
from setuptools import setup

setup(
  name="jupyslack",
  version="0.2.1",
  packages=["jupyslack"],
  license="MIT",
  author="Adrien Chuttarsing",
  author_email="adrien.chuttarsing@gmail.com",
  url="https://github.com/Achuttarsing/jupyslack",
  description="Slack integration to notebooks",
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  keywords="ipython slack notebook jupyslack",
  install_requires = ['ipython','requests'],
  classifiers=[
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "Framework :: IPython",
      "Programming Language :: Python",
      "Topic :: Utilities",
  ],
)
