__author__ = 'Xuanli Chen'
"""
Xuanli Chen
PhD student at PSI-VISICS, KU Leuven
Supervisor: Prof. Luc Van Gool
Focus Domain: Machine Learning, Music, Computer Vision
Email: xuanli.chen@esat.kuleuven.be

Address:
Kasteelpark Arenberg 10 - bus 2441
B-3001 Heverlee
Belgium

Group website: http://www.esat.kuleuven.be/psi/visics
LinkedIn: https://be.linkedin.com/in/xuanlichen
"""
from setuptools import setup

setup(name='alamire_of_tamir',
      version='0.11',
      description='Translate the manuscripts',
      # long_description=readme(),
      # classifiers=[
      #     'License :: OSI Approved :: GNU License',
      #     'Programming Language :: Python :: 2.7',
      #     'Topic :: Computer Vision :: Manuscript Transcription',
      # ],
      keywords='Manuscript Transcription, Alamire, TAMIR',
      url='https://github.com/zb8c5ek/alamire_of_tamir.git',
      author='Xuanli Chen',
      author_email='xuanli.chen@esat.kuleuven.be',
      license='MIT',
      packages=['alamire_of_tamir'],
      install_requires=[
          'music21', 'numpy'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
          # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      entry_points={
          'console_scripts': ['alamire_translation=alamire_of_tamir.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
