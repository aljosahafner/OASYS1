#! /usr/bin/env python3

import imp
import os
import sys
import subprocess

NAME = 'Orange'

VERSION = '4.0'
ISRELEASED = False

DESCRIPTION = 'Shadow, Ray-tracing simulation software'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'Luca Rebuffi, Manuel Sanchez del Rio and Bioinformatics Laboratory, FRI UL'
AUTHOR_EMAIL = 'luca.rebuffi@elettra.eu'
URL = 'http://orange.biolab.si/'
DOWNLOAD_URL = 'https://bitbucket.org/biolab/orange/downloads'
LICENSE = 'GPLv3'

KEYWORDS = (
    'data mining',
    'machine learning',
    'artificial intelligence',
)

CLASSIFIERS = (
    'Development Status :: 4 - Beta',
    'Environment :: X11 Applications :: Qt',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Python',
    'Framework :: Orange',
    'License :: OSI Approved :: '
    'GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
)

INSTALL_REQUIRES = (
    'setuptools',
    'numpy',
    'scipy',
    'bottleneck'
)

if len({'develop', 'release', 'bdist_egg', 'bdist_rpm', 'bdist_wininst',
        'install_egg_info', 'build_sphinx', 'egg_info', 'easy_install',
        'upload', 'test'}.intersection(sys.argv)) > 0:
    import setuptools
    extra_setuptools_args = dict(
        zip_safe=False,  # the package can run out of an .egg file
        include_package_data=True,
        test_suite='Orange.tests.test_suite',
        install_requires=INSTALL_REQUIRES
    )
else:
    extra_setuptools_args = dict()


# Return the git revision as a string
def git_version():
    """Return the git revision as a string.

    Copied from numpy setup.py
    """
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout = subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION

def write_version_py(filename='Orange/version.py'):
    # Copied from numpy setup.py
    cnt = """
# THIS FILE IS GENERATED FROM ORANGE SETUP.PY
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
    short_version += ".dev"
"""
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    elif os.path.exists('Orange/version.py'):
        # must be a source distribution, use existing version file
        version = imp.load_source("Orange.version", "Orange/version.py")
        GIT_REVISION = version.git_revision
    else:
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev-' + GIT_REVISION[:7]

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()

from numpy.distutils.core import setup

def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    # Avoid non-useful msg:
    # "Ignoring attempt to set 'name' (from ... "
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('Orange')

    config.get_version('Orange/version.py')  # sets config.version

    return config


def all_with_extension(path, extensions):
    return [os.path.join(path, "*.%s" % extension) for extension in extensions]


def setup_package():
    write_version_py()
    setup(
        configuration=configuration,
        name=NAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        download_url=DOWNLOAD_URL,
        license=LICENSE,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        package_data={
            "Orange": all_with_extension(path="datasets", extensions=("tab", "csv", "basket")),
            "Orange.canvas": ["icons/*.png", "icons/*.svg", "WidgetTabs.txt"],
            "Orange.canvas.styles": ["*.qss", "orange/*.svg"],
            "Orange.canvas.application.tutorials": ["*.ows"],
            "Orange.shadow.argonne11bm_absorption": ["*.dat"],
            "Orange.widgets": ["icons/*.png"],
            "Orange.widgets.shadow_experimental_elements": ["icons/*.png"],
            "Orange.widgets.shadow_optical_elements": ["icons/*.png"],
            "Orange.widgets.shadow_plots": ["icons/*.png", "icons/*.jpg"],
            "Orange.widgets.shadow_preprocessor": ["icons/*.png", "icons/*.jpg"],
            "Orange.widgets.shadow_sources": ["icons/*.png"],
            "Orange.widgets.shadow_user_defined": ["icons/*.png", "icons/*.jpg"],
            "Orange.widgets.data": ["icons/*.svg", "icons/paintdata/*.png", "icons/paintdata/*.svg"],
            "Orange.widgets.visualize": ["icons/*.svg"],
            "Orange.widgets.plot": ["*.fs", "*.gs", "*.vs"],
            "Orange.widgets.plot.primitives": ["*.obj"],
        },
        packages=["Orange",
                  "Orange.canvas",
                  "Orange.canvas.application",
                  "Orange.canvas.application.tutorials",
                  "Orange.canvas.canvas",
                  "Orange.canvas.canvas.items",
                  "Orange.canvas.document",
                  "Orange.canvas.gui",
                  "Orange.canvas.help",
                  "Orange.canvas.preview",
                  "Orange.canvas.registry",
                  "Orange.canvas.scheme",
                  "Orange.canvas.styles",
                  "Orange.canvas.utils",
                  "Orange.classification",
                  "Orange.data",
                  "Orange.data.sql",
                  "Orange.evaluation",
                  "Orange.feature",
                  "Orange.misc",
                  "Orange.shadow",
                  "Orange.shadow.argonne11bm_absorption",
                  "Orange.statistics",
                  "Orange.testing",
                  "Orange.widgets",
                  "Orange.widgets.data",
                  "Orange.widgets.shadow_experimental_elements",
                  "Orange.widgets.shadow_gui",
                  "Orange.widgets.shadow_optical_elements",
                  "Orange.widgets.shadow_plots",
                  "Orange.widgets.shadow_preprocessor",
                  "Orange.widgets.shadow_sources",
                  "Orange.widgets.shadow_user_defined",
                  "Orange.widgets.utils",
                  "Orange.widgets.utils.plot",
                  "Orange.widgets.utils.plot.primitives",
                  "Orange.widgets.visualize"],
        **extra_setuptools_args
    )

if __name__ == '__main__':
    setup_package()
