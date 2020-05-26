# import mapactionpy_controller.config_verify as config_verify
from time import sleep
import humanfriendly.terminal as hft
from humanfriendly.terminal.spinners import AutomaticSpinner
import logging
import random

logger = logging.getLogger('MapChef')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)


class Step():
    def __init__(self, func, running_msg, complete_msg, fail_msg):
        self.func = func
        self.running_msg = running_msg
        self.complete_msg = complete_msg
        self.fail_msg = fail_msg

    def run(self, set_status, verbose, **kwargs):
        try:
            result = self.func(*kwargs)
            if verbose:
                msg = '{}\n{}'.format(self.complete_msg, result)
            else:
                msg = self.complete_msg

            set_status(logging.INFO, msg)
            return result
            # return True
        except Exception as exp:
            fail_msg = '{}\n{}'.format(self.fail_msg, exp)
            set_status(logging.ERROR, fail_msg)


def line_printer(status, msg):
    bright_white = hft.ansi_style(color='white', bright=True)
    bright_green = hft.ansi_style(color='green', bright=True)
    bright_red = hft.ansi_style(color='red', bright=True)
    bright_yellow = hft.ansi_style(color='yellow', bright=True)
    normal_white = hft.ansi_style(color='white', bright=False)

    checkboxs = {
        logging.INFO:  '{}[{}pass{}]{}'.format(normal_white, bright_green, normal_white, bright_white),
        logging.ERROR: '{}[{}fail{}]{}'.format(normal_white, bright_red, normal_white, bright_white),
        logging.WARNING: '{}[{}warn{}]{}'.format(normal_white, bright_yellow, normal_white, bright_white)
    }

    if hft.connected_to_terminal():
        hft.output('{} {} {}'.format(hft.ANSI_ERASE_LINE, checkboxs[status], msg))
    else:
        logger.log(status, msg)


def process_steps(step_list):
    hft.enable_ansi_support()

    for step in step_list:
        if hft.connected_to_terminal():
            with AutomaticSpinner(step.running_msg, show_time=True):
                step.run(line_printer, False)
        else:
            logger.info('Starting: {}'.format(step.running_msg))
            step.run(line_printer, False)


def get_demo_steps(secs=3):
    def random_pass():
        sleep(secs)
        if random.random() > 0.5:
            raise ValueError('Something went wrong')

        return 'stopped for {} secs'.format(secs)

    demo_steps = [
        Step(
            random_pass,
            'DEMO: Checking that the Crash Move Folder description file opens correctly',
            'DEMO: The Crash Move Folder description file opened correctly',
            'DEMO: Failed to open the Crash Move Folder description file correctly',
        ),
        Step(
            random_pass,
            'DEMO: Checking that each of the configuration files matches their relevant schemas',
            'DEMO: Each of the configuration files adheres to their relevant schemas',
            'DEMO: Failed to verify one or more of the configuration files against the relevant schema',
        ),
        Step(
            random_pass,
            'DEMO: Comparing the contents of the layer properties json file and the layer rendering directory',
            'DEMO: Compared the contents of the layer properties json file and the layer rendering directory',
            'DEMO: Inconsistancy found in between the contents of the layer properties json file and the layer'
            ' rendering directory'
        ),
        Step(
            random_pass,
            'DEMO: Comparing the contents of the layer properties json file and the MapCookbook',
            'DEMO: Compared the contents of the layer properties json file and the MapCookbook',
            'DEMO: Inconsistancy found in between the contents of the layer properties json file and the MapCookbook'
        )
    ]

    return demo_steps


if __name__ == "__main__":
    process_steps(get_demo_steps())
