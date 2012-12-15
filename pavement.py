from paver.easy import *


@task
def test():
    sh("python2.6 tests.py")
    sh("python2.7 tests.py")
    sh("python3.3 tests.py")


@task
def upload():
    sh("python setup.py register")
    sh("python setup.py sdist upload")