# import mapactionpy_controller.config_verify as config_verify
from time import sleep
import humanfriendly.terminal as hft
from humanfriendly.terminal.spinners import AutomaticSpinner
import random


class Step():
    def __init__(self, func, running_msg, complete_msg, fail_msg):
        self.func = func
        self.running_msg = running_msg
        self.complete_msg = complete_msg
        self.fail_msg = fail_msg

    def run(self, set_status, **kwargs):
        try:
            # set_status('running', self.running_msg)
            result = self.func(*kwargs)
            # sleep(5)
            # if random.random() > 0.5:
            #    raise ValueError('Something went wrong')

            set_status('pass', self.complete_msg)
            return result
            # return True
        except Exception as exp:
            fail_msg = '{}\n{}'.format(self.fail_msg, exp)
            set_status('fail', fail_msg)


# cv = config_verify.ConfigVerifier()


def line_printer(status, msg):
    bright_white = hft.ansi_style(color='white', bright=True)
    bright_green = hft.ansi_style(color='green', bright=True)
    bright_red = hft.ansi_style(color='red', bright=True)
    normal_white = hft.ansi_style(color='white', bright=False)

    checkboxs = {
        'pass':    '{}[{}pass{}]{}'.format(normal_white, bright_green, normal_white, bright_white),
        'fail':    '{}[{}fail{}]{}'.format(normal_white, bright_red, normal_white, bright_white)
    }

    str = ' {} {}'.format(checkboxs[status], msg)

    hft.output('{}{}'.format(hft.ANSI_ERASE_LINE, str))


def process_steps(step_list):
    hft.enable_ansi_support()

    for step in step_list:
        with AutomaticSpinner(step.running_msg, show_time=True):
            step.run(line_printer)


if __name__ == "__main__":
    process_steps(config_verify_steps)
