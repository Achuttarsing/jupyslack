  # setup.py
  from setuptools import setup

  setup(
      name="Jupyslack",
      version="0.1",
      packages=["jupyslack"],
      license="MIT",
      author="Adrien Chuttarsing",
      author_email="adrien.chuttarsing@gmail.com",
      url="https://github.com/Achuttarsing/jupyslack",
      description="Slack integration to notebooks",
      long_description=open("README.md").read(),
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
