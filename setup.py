from setuptools import setup
"""
Xuanli Chen
PhD student at PSI-VISICS, KU Leuven
Supervisor: Prof. Luc Van Gool
Research Domain: Computer Vision, Machine Learning
Address:
Kasteelpark Arenberg 10 - bus 2441
B-3001 Heverlee
Belgium
Group website: http://www.esat.kuleuven.be/psi/visics
LinkedIn: https://be.linkedin.com/in/xuanlichen
"""
setup(name='alamire_of_tamir',
      version='0.15.1',
      description='Translate the manuscripts',
      url='https://github.com/zb8c5ek/alamire_of_tamir',
      keywords='Manuscript Transcription, Alamire, TAMIR',

      author='RemovedAuthorInformationDueToDoubleBlindReview',
      author_email='RemovedAuthorContactDueToDoubleBlindReview',
      license='MIT',
      classifiers=[
          'License :: OSI Approved :: MIT License',

          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',

      ],
      packages=['alamire_of_tamir'],
      install_requires=[
          'music21', 'numpy'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
          'console_scripts': ['alamire_translation=alamire_of_tamir.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
