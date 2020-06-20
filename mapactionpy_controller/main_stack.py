# import mapactionpy_controller.config_verify as config_verify
import humanfriendly.terminal
import logging
from humanfriendly.terminal.spinners import AutomaticSpinner

# logging.basicConfig(
#     level=logging.DEBUG,
#     format=(
#         '%(asctime)s %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s'
#         ' [%(process)d] %(message)s',
#     )
# )

logger = logging.getLogger('MapChef')
# logger = logging.getLogger()
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s (%(module)s +ln%(lineno)s) ;- %(message)s')
# formatter = logging.Formatter('%(asctime)s %(module)s %(name)s.%(funcName)s
# +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')

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


def get_jira_client():
    try:
        from mapactionpy_controller.jira_tasks import JiraClient
        return JiraClient()
    except ImportError:
        return None


jira_client = get_jira_client()


def line_printer(status, msg, step, **kwargs):
    if jira_client:
        jira_client.task_handler(status, msg, step, **kwargs)
    else:
        print('Cant load JIRA but would call it with status="{}", step.func=`{}` and msg="{}"'.format(
            status, step.func.__name__, msg
        ))

    if humanfriendly.terminal.connected_to_terminal():
        humanfriendly.terminal.output('{} {} {}'.format(
            humanfriendly.terminal.ANSI_ERASE_LINE,
            terminal_checkboxs[status],
            msg)
        )
    else:
        logger.log(status, msg)


def process_stack(step_list, initial_state):
    humanfriendly.terminal.enable_ansi_support()
    state = initial_state

    # TODO this should be a stack not a list
    # https://realpython.com/how-to-implement-python-stack/
    # and
    # https://docs.python.org/2/tutorial/datastructures.html#using-lists-as-stacks
    for step in step_list:
        kwargs = {'state': state}

        if humanfriendly.terminal.connected_to_terminal():
            with AutomaticSpinner(step.running_msg, show_time=True):
                state = step.run(line_printer, False, **kwargs)
        else:
            logger.info('Starting: {}'.format(step.running_msg))
            state = step.run(line_printer, False, **kwargs)

    return state
