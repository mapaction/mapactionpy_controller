# import mapactionpy_controller.config_verify as config_verify
from collections import deque
import humanfriendly.terminal
import logging
from humanfriendly.terminal.spinners import AutomaticSpinner
from mapactionpy_controller.steps import Step
import itertools

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


# def get_jira_client():
#     try:
#         import mapactionpy_controller.jira_tasks
#         return mapactionpy_controller.jira_tasks.jira_client
#     except ImportError:
#         return None


# jira_client = get_jira_client()

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


def _add_steps_from_state_to_stack(new_state, stack, old_state):
    if isinstance(new_state, Step):
        stack.append(new_state)
        return old_state

    if isinstance(new_state, list) and all([isinstance(stp, Step) for stp in new_state]):
        new_state.reverse()
        stack.extend(new_state)
        return old_state

    return new_state


def process_stack(step_list, initial_state):
    humanfriendly.terminal.enable_ansi_support()
    n_state = initial_state
    step_list.reverse()
    stack = deque(step_list)

    while stack:
        # Definitions
        # n_state = the state for the current iteration
        # nplus_state = the state for the next iteraction (eg N+1)
        step = stack.pop()
        kwargs = {'state': n_state}
        # print('kwargs = {}'.format(kwargs))
        # print('len(kwargs) = {}'.format(len(kwargs)))

        if humanfriendly.terminal.connected_to_terminal():
            with AutomaticSpinner(step.running_msg, show_time=True):
                nplus_state = step.run(line_printer, False, **kwargs)
        else:
            logger.info('Starting: {}'.format(step.running_msg))
            nplus_state = step.run(line_printer, False, **kwargs)

        n_state = _add_steps_from_state_to_stack(nplus_state, stack, n_state)

    return n_state
