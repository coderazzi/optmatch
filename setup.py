from distutils.core import setup

optmatch_version = '0.9.1'
setup(
    name='optmatch',
    packages=['optmatch'],  # this must be the same as the name above
    version=optmatch_version,
    description='command line parsing library',
    author='coderazzi <LuisM Pena>',
    author_email='coderazzi@gmail.com',
    url='http://coderazzi.net/python/optmatch',  # use the URL to the github repo
    download_url='http://coderazzi.net/python/optmatch/optmatch-%s.tar.gz' % optmatch_version,
    keywords=['args', 'parsing', 'easy'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
