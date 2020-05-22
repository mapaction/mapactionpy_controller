import mapactionpy_controller.config_verify as config_verify
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
            # result = self.func(*kwargs)
            sleep(5)
            if random.random() > 0.5:
                raise ValueError('Something went wrong')

            set_status('pass', self.complete_msg)
            # return result
            return True
        except Exception as exp:
            fail_msg = '{}\n{}'.format(self.fail_msg, exp)
            set_status('fail', fail_msg)


cv = config_verify.ConfigVerifier()

config_verify_steps = [
    Step(
        cv.check_cmf_description,
        'Checking that the Crash Move Folder description file opens correctly',
        'The Crash Move Folder description file opened correctly',
        'Failed to open the Crash Move Folder description file correctly',
    ),
    Step(
        cv.check_json_file_schemas,
        'Checking that each of the configuration files matches their relevant schemas',
        'Each of the configuration files adheres to their relevant schemas',
        'Failed to verify one or more of the configuration files against the relevant schema',
    ),
    Step(
        cv.check_lyr_props_vs_rendering_dir,
        'Comparing the contents of the layer properties json file and the layer rendering directory',
        'Compared the contents of the layer properties json file and the layer rendering directory',
        'Inconsistancy found in between the contents of the layer properties json file and the layer rendering directory'
    ),
    Step(
        cv.check_lyr_props_vs_map_cookbook,
        'Comparing the contents of the layer properties json file and the MapCookbook',
        'Compared the contents of the layer properties json file and the MapCookbook',
        'Inconsistancy found in between the contents of the layer properties json file and the MapCookbook'
    )
]


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

    # humanfriendly.terminal.output(humanfriendly.terminal.ANSI_ERASE_LINE)
    hft.output('{}{}'.format(hft.ANSI_ERASE_LINE, str))


def steps_to_run():
    hft.enable_ansi_support()

    for step in config_verify_steps:
        with AutomaticSpinner(step.running_msg, show_time=True):
            step.run(line_printer)


if __name__ == "__main__":
    steps_to_run()
