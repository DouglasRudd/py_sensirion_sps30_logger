from setuptools import setup

setup(
  name = 'py_sensirion_sps30_logger',
  version = '0.0.002',
  description = 'A programme to log data from Sensirion SPS30 particulate matter sensors',
  url = 'http://github.com/skgrange/py_sensirion_sps30_logger',
  author = 'Stuart K. Grange',
  author_email = 's.k.grange@gmail.com',
  license = 'GPL-3 | file LICENSE',
  packages = ['py_sensirion_sps30_logger'],
  install_requires = ['pytz', 'pyserial'],
  scripts = ['bin/log_sensirion_sps30_sensor'],
  zip_safe = True
)

