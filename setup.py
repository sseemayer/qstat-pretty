from distutils.core import setup

setup(
    name='qstat-pretty',
    version='0.1.0',
    author='Stefan Seemayer',
    author_email='stefan@seemayer.de',
    license='GPL',
    url='https://github.com/sseemayer/qstat-pretty',

    packages=['qstatpretty', 'qstatpretty.ttyutil'],
    scripts=['pstat']
)
