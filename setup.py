from setuptools import setup

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
