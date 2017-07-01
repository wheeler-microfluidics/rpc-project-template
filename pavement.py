from collections import OrderedDict
import sys
from importlib import import_module

from paver.easy import path, options
from paver.setuputils import install_distutils_tasks
import platformio_helpers as pioh
import platformio_helpers.develop
try:
    from base_node_rpc.pavement_base import *
except ImportError:
    import warnings

    warnings.warn('Could not import `base_node_rpc` (expected during '
                  'install).')

sys.path.insert(0, '.')
import version
install_distutils_tasks()

DEFAULT_ARDUINO_BOARDS = ['uno']
PROJECT_PREFIX = 'rpc_project_template'
module_name = PROJECT_PREFIX
package_name = module_name.replace('_', '-')
rpc_module = import_module(PROJECT_PREFIX)
VERSION = version.getVersion()
URL='http://github.com/wheeler-microfluidics/%s.git' % package_name
PROPERTIES = OrderedDict([('package_name', package_name),
                          ('display_name', package_name),
                          ('manufacturer', 'Wheeler Lab'),
                          ('software_version', VERSION),
                          ('url', URL)])
LIB_PROPERTIES = PROPERTIES.copy()
LIB_PROPERTIES.update(OrderedDict([('author', 'Christian Fobel'),
                                   ('author_email', 'christian@fobel.net'),
                                   ('short_description', 'Template project '
                                    'demonstrating use of Arduino base node '
                                    'RPC framework.'),
                                   ('version', VERSION),
                                   ('long_description', ''),
                                   ('category', 'Communication'),
                                   ('architectures', 'avr')]))

options(
    rpc_module=rpc_module,
    PROPERTIES=PROPERTIES,
    LIB_PROPERTIES=LIB_PROPERTIES,
    base_classes=['BaseNodeSerialHandler',
                  'BaseNodeEeprom',
                  'BaseNodeI2c',
                  'BaseNodeI2cHandler<Handler>',
                  'BaseNodeConfig<ConfigMessage, Address>',
                  'BaseNodeState<StateMessage>'],
    rpc_classes=['rpc_project_template::Node'],
    DEFAULT_ARDUINO_BOARDS=DEFAULT_ARDUINO_BOARDS,
    setup=dict(name=package_name,
               version=VERSION,
               description=LIB_PROPERTIES['short_description'],
               author='Christian Fobel',
               author_email='christian@fobel.net',
               url=URL,
               license='GPLv2',
               install_requires=['base-node-rpc>=0.12.post23'],
               include_package_data=True,
               packages=[str(PROJECT_PREFIX)]))

@task
def develop_link():
    import logging; logging.basicConfig(level=logging.INFO)
    pioh.develop.link(working_dir=path('.').realpath(),
                      package_name=package_name)


@task
def develop_unlink():
    import logging; logging.basicConfig(level=logging.INFO)
    pioh.develop.unlink(working_dir=path('.').realpath(),
                        package_name=package_name)


@task
@needs('generate_all_code')
def build_firmware():
    sh('pio run')


@task
def upload():
    sh('pio run --target upload --target nobuild')
