from setuptools import setup

setup(name='alamire_of_tamir',
      version='0.12',
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
