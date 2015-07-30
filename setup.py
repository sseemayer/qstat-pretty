from distutils.core import setup

setup(
    name='qstat-pretty',
    version='0.0.1',
    author='Stefan Seemayer',
    author_email='stefan@seemayer.de',
    license='MIT',
    url='https://github.com/sseemayer/qstat-pretty',

    packages=['qstatpretty', 'qstatpretty.ttyutil'],
    scripts=['pstat']
)
