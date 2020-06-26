# import mapactionpy_controller.config_verify as config_verify
from collections import deque
import humanfriendly.terminal
import logging
from humanfriendly.terminal.spinners import AutomaticSpinner
from mapactionpy_controller.steps import Step

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
    """
    This is called once per step execution.
    It provides a hook into print messages to the terminal, log files and the JIRA Client.
    """
    # nice_output = '{}\n{}'.format(self.complete_msg, result)
    # pass_back['result'] = str(result)
    # useful_output = '{}\n{}'.format(self.fail_msg, exp)
    # pass_back['result'] = str(exp)
    # pass_back['exp'] = exp

    # the_msg = '\n'.join([msg, kwargs.get('result', ''),  kwargs.get('exp', '')])
    the_msg='{}\nresult={}\nexp={}'.format(msg, kwargs.get('result', ''),  kwargs.get('exp', ''))

    if jira_client:
        jira_client.task_handler(status, msg, step, **kwargs)
    # else:
    #     logging.debug('Cant load JIRA but would call it with status="{}", step.func=`{}` and msg="{}"'.format(
    #         status, step.func.__name__, msg
    #     ))

    if humanfriendly.terminal.connected_to_terminal():
        humanfriendly.terminal.output('{} {} {}'.format(
            humanfriendly.terminal.ANSI_ERASE_LINE,
            terminal_checkboxs[status],
            the_msg)
        )
    else:
        logger.log(status, the_msg)


def _add_steps_from_state_to_stack(new_state, stack, old_state):
    """
    This helper function checks to see Step has returned one or more addtional Steps. If so these
    are added to the top of the stack.

    :param new_state: The return value of the most recently called Step object.
    :param stack: The stack.
    :param old_state: The state value which was passed to the most recently called Step object.
    :returns: If `new_state` contains Step objects then `old_state` is returned. Else `new_state`
       is returned
    """
    if isinstance(new_state, Step):
        stack.append(new_state)
        return old_state

    if isinstance(new_state, list) and all([isinstance(stp, Step) for stp in new_state]):
        new_state.reverse()
        stack.extend(new_state)
        return old_state

    return new_state


def process_stack(step_list, initial_state):
    """
    This is the principal function which executes the stack of `Step` objects. For each step in the stack
    its `func` is called.
    * If `func` returns one or more Step objects (either as a single object or as a list) then these are
      added to the top of the stack. The `state` remains unaltered and is passed to the next Step.
    * If `func` returns any other value (including None and other falsey values) then this is passed as
      the state object to the `func` of the next Step item in the stack.

    :param step_list: A list of initial steps which are used to populate the stack.
    :param initial_state: This value will be passed a the 'state' keyword arg to the first step's `func`.
    :returns: The return value of the final step's `func`.
    """
    humanfriendly.terminal.enable_ansi_support()
    n_state = initial_state
    step_list.reverse()
    stack = deque(step_list)

    while stack:
        # Definitions:
        # `n_state` = the state for the current iteration
        # `nplus_state` = the state for the next iteraction (eg N+1)
        step = stack.pop()
        kwargs = {'state': n_state}

        if humanfriendly.terminal.connected_to_terminal():
            with AutomaticSpinner(step.running_msg, show_time=True):
                nplus_state = step.run(line_printer, **kwargs)
        else:
            logger.info('Starting: {}'.format(step.running_msg))
            nplus_state = step.run(line_printer, **kwargs)

        # Used to increment the state *only* if no new Steps where returned
        n_state = _add_steps_from_state_to_stack(nplus_state, stack, n_state)

    return n_state
