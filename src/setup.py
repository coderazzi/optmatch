from distutils.core import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='optmatch',
    py_modules=['optmatch'],
    version='1.0.0',
    description='command line parsing library',
    author='coderazzi (LuisM Pena)',
    author_email='coderazzi@gmail.com',
    url='http://coderazzi.net/python/optmatch',
    long_description=readme(),
    keywords=['args', 'parsing', 'easy'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
