from setuptools import setup, find_packages

setup(name='pypacman',
      version='0.7',
      description='Pacman game written in python',
      url='https://github.com/denix666/pypacman',
      author='Denis Salmanovich',
      author_email='denis.salmanovich@gmail.com',
      include_package_data=True,
      license='GPLv3',
      packages=find_packages(),
      package_data={
        '': ['*.ttf', '*.png', '*.ogg', '*.mp3', '*.wav', '*.json'],
      },
      requires=[
        'python (>=3.8.0)',
        'arcade (>=2.6.8)',
        ],
      zip_safe=False,
      entry_points={
          'console_scripts': ['pypacman=pypacman.__main__:main'],
      }
      )
