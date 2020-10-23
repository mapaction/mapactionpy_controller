"""
# main_stack

The main stack within `mapaction_controller` exists in two modules; this one and steps.py. Each individual
step is represented by a Step object, which is a wrapper for:

* A function to run (which must accept kwargs**).
* A definition of a "running", "success" and "failure" message.
* A severity of failure.

The main function in main_stack.py is `process_stack()`, which works through a list of "Step" objects. For
each Step:

    * Its function is called.
    * The function may return:
        - One or more new Step objects (which are inserted into the slack). Closures are very useful here
        - An updated state object (which will passed to the next step)
    * Each Step defines each of a "running", "success" and "failure" message, which is displayed on the
      console and/or log as appropriate.


Execution continous until there are no more Steps.

Note: main_stack.py also includes humanfriendly.terminal which ought really to be part of the CLI.
"""
import logging
import traceback
from collections import deque

import humanfriendly.terminal as hft
import humanfriendly.terminal.spinners as spinners

from mapactionpy_controller.steps import Step

logger = logging.getLogger(__name__)

bright_white = hft.ansi_style(color='white', bright=True)
bright_green = hft.ansi_style(color='green', bright=True)
bright_red = hft.ansi_style(color='red', bright=True)
bright_yellow = hft.ansi_style(color='yellow', bright=True)
normal_white = hft.ansi_style(color='white', bright=False)

terminal_checkboxs = {
    logging.INFO:  '{}[{}pass{}]{}'.format(normal_white, bright_green, normal_white, bright_white),
    logging.ERROR: '{}[{}fail{}]{}'.format(normal_white, bright_red, normal_white, bright_white),
    logging.WARNING: '{}[{}warn{}]{}'.format(normal_white, bright_yellow, normal_white, bright_white)
}


def get_jira_client():
    try:
        from mapactionpy_controller.jira_tasks import JiraClient
        return JiraClient()
    except (ImportError, ValueError):
        return None


jira_client = get_jira_client()


def parse_feedback(status, msg, step, **kwargs):
    """
    This is called once per step execution.
    It provides a hook into print messages to the terminal, log files and the JIRA Client.
    """
    # nice_output = '{}\n{}'.format(self.complete_msg, result)
    # pass_back['result'] = result
    # pass_back['exp'] = exp

    the_msg = msg
    task_referal = None
    if status > logging.INFO:
        exp = kwargs['exp']
        task_referal = exp.args[0]

    if status > logging.WARNING:
        stack_trace = kwargs['stack_trace']
        the_msg = '{}\nerror message={}\n{}\n{}'.format(
            msg, str(type(exp)), str(exp.args), stack_trace)

    if jira_client:
        jira_client.task_handler(status, msg, task_referal)

    if hft.connected_to_terminal():
        hft.output('{} {} {}'.format(
            hft.ANSI_ERASE_LINE,
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
    hft.enable_ansi_support()
    n_state = initial_state
    step_list.reverse()
    stack = deque(step_list)

    try:
        while stack:
            # Definitions:
            # `n_state` = the state for the current iteration
            # `nplus_state` = the state for the next iteraction (eg N+1)
            step = stack.pop()
            kwargs = {'state': n_state}

            if hft.connected_to_terminal():
                with spinners.AutomaticSpinner(step.running_msg, show_time=True):
                    nplus_state = step.run(parse_feedback, **kwargs)
            else:
                logger.info('Starting: {}'.format(step.running_msg))
                nplus_state = step.run(parse_feedback, **kwargs)

            # Used to increment the state *only* if no new Steps where returned
            n_state = _add_steps_from_state_to_stack(nplus_state, stack, n_state)

        return n_state
    except Exception as exp:
        pass_back = {
            'exp': exp,
            'stack_trace': traceback.format_exc()
        }

        print(pass_back)

        parse_feedback(logging.ERROR, 'Unable to continue following the previous error', None, **pass_back)
