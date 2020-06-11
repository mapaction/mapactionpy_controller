# import mapactionpy_controller.config_verify as config_verify
from time import sleep
from humanfriendly.terminal.spinners import AutomaticSpinner
import humanfriendly.terminal
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

bright_white = humanfriendly.terminal.ansi_style(color='white', bright=True)
bright_green = humanfriendly.terminal.ansi_style(color='green', bright=True)
bright_red = humanfriendly.terminal.ansi_style(color='red', bright=True)
bright_yellow = humanfriendly.terminal.ansi_style(color='yellow', bright=True)
normal_white = humanfriendly.terminal.ansi_style(color='white', bright=False)

terminal_checkboxs = {
    logging.INFO:  '{}[{}pass{}]{}'.format(normal_white, bright_green, normal_white, bright_white),
    logging.ERROR: '{}[{}fail{}]{}'.format(normal_white, bright_red, normal_white, bright_white),
    logging.WARNING: '{}[{}warn{}]{}'.format(normal_white, bright_yellow, normal_white, bright_white)
}


class Step():
    def __init__(self, func, running_msg, complete_msg, fail_msg):
        self.func = func
        self.running_msg = running_msg
        self.complete_msg = complete_msg
        self.fail_msg = fail_msg

    def run(self, set_status, verbose, previous_state=None, **kwargs):
        try:
            args = kwargs.copy()
            if previous_state:
                args['recipe'] = previous_state

            result = self.func(**args)
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
    if humanfriendly.terminal.connected_to_terminal():
        humanfriendly.terminal.output('{} {} {}'.format(
            humanfriendly.terminal.ANSI_ERASE_LINE,
            terminal_checkboxs[status],
            msg)
        )
    else:
        logger.log(status, msg)


def process_steps(step_list, initial_state=None):
    humanfriendly.terminal.enable_ansi_support()
    state = initial_state

    for step in step_list:
        if humanfriendly.terminal.connected_to_terminal():
            with AutomaticSpinner(step.running_msg, show_time=True):
                state = step.run(line_printer, False, previous_state=state)
        else:
            logger.info('Starting: {}'.format(step.running_msg))
            step.run(line_printer, False)

    return state


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
