# Copyright 2016 Yanis Guenane <yguenane@redhat.com>
# Author: Yanis Guenane <yguenane@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import codecs
import os
import setuptools

from lecm import version


def _get_requirements():
    requirements_path = '%s/%s' % (os.path.dirname(os.path.abspath(__file__)),
                                   'requirements.txt')
    with open(requirements_path, 'r') as f:
        requirements = f.read()
        # remove the dependencies which comes from url source because
        # it's not supported by install_requires
        return [dep for dep in requirements.split('\n')
                if not dep.startswith('-e')]


def _get_readme():
    readme_path = '%s/%s' % (os.path.dirname(os.path.abspath(__file__)),
                             'README.rst')

    with codecs.open(readme_path, 'r', encoding='utf8') as f:
        return f.read()


setuptools.setup(
    name='lecm',
    version=version.__version__,
    packages=setuptools.find_packages(),
    author='Yanis Guenane',
    author_email='yguenane@redhat.com',
    description='Tool to manage Let''s Encrypt certificates \
                  from configuration file',
    long_description=_get_readme(),
    install_requires=_get_requirements(),
    url='https://github.com/redhat-cip/lecm',
    license='Apache v2.0',
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'lecm = lecm.shell:main'
        ],
    }
)
