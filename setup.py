from pathlib import Path

from setuptools import setup

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='midsearch',
      version='0.0.1',
      description='Python client for Midsearch',
      packages=['midsearch.client'],
      install_requires=[
          'click==8.0.4',
          'discord.py==2.2.3',
          'graia-ariadne==0.11.5',
          'python-dotenv==0.21.0',
          'python-telegram-bot==20.2'
      ],
      scripts=['bin/midsearch'],
      long_description=long_description,
      long_description_content_type='text/markdown'
      )
