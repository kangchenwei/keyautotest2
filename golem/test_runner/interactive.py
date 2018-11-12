"""Golem interactive mode."""
import golem.core
from golem.core import utils
from golem import actions
from golem import execution
from golem.actions import *
# TODO remove wild card import
from golem import browser
from golem.core.test_execution import cli_drivers, settings


def interactive(settings, cli_drivers):
	#Starts the Golem interactive shell.
    drivers = utils.choose_driver_by_precedence(cli_drivers=cli_drivers,
                                                suite_drivers=[],
                                                settings_default_driver=settings['default_browser'])
    execution.browser_name = drivers[0]
    #golem.core.set_settings(settings)
    execution.settings = settings
    from golem.core import execution_logger
    execution.logger = execution_logger.get_logger()
    actions.debug()