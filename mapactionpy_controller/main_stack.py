# import mapactionpy_controller.config_verify as config_verify
from collections import deque
import humanfriendly.terminal as hft
import logging
# from humanfriendly.terminal.spinners import AutomaticSpinner
import humanfriendly.terminal.spinners as spinners
from mapactionpy_controller.steps import Step
import traceback

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
    except ImportError:
        return None


jira_client = get_jira_client()


def line_printer(status, msg, step, **kwargs):
    """
    This is called once per step execution.
    It provides a hook into print messages to the terminal, log files and the JIRA Client.
    """
    # nice_output = '{}\n{}'.format(self.complete_msg, result)
    # pass_back['result'] = result
    # pass_back['exp'] = exp

    the_msg = msg
    if status > logging.WARNING:
        exp = kwargs['exp']
        stack_trace = kwargs['stack_trace']
        the_msg = '{}\nerror message={}\n{}\n{}'.format(
            msg, str(type(exp)), str(exp.args), stack_trace)

    if jira_client:
        jira_client.task_handler(status, msg, step, **kwargs)

    if hft.connected_to_terminal():
        hft.output('{} {} {}'.format(
            hft.ANSI_ERASE_LINE,
            terminal_checkboxs[status],
            the_msg)
        )
    else:
        logger.log(status, the_msg)


def translate_into_task(status, step, **kwargs):
    """
    Returns the "dict of values" used by the mustache rendering
    """
    if status < logging.WARNING:
        # We just have an "INFO"
        # Therefore expect this kwarg:
        state = kwargs['result']
    else:
        # Something more serious
        # Therefore expect these kwargs:
        exp = kwargs['exp']
        stack_trace = kwargs['stack_trace']
        # This _may_ be present but not guaranteed
        state = kwargs.get('result', None)

    # In each case there may be a single item OR a list of items. If it is a list of items
    # then there will be one JIRA task per item in the list.
    mustache_template_lookup = {
        # A `NameResult` object
        'check_gis_data_name': 'name_result',

        # A tuple or class representing the misplaced file (to be implenmented)
        'check_file_in_wrong_directory': 'misplace_file_list',

        # A RecipeLayer object (with detailed adapted from MapResult)
        'update_recipe_with_datasources': 'gis-data-missing',

        # A tuple of RecipeLayer object (with detailed adapted from MapResult)
        # and a ValidationError
        'check_data_schema': 'schema_error',

        # A RecipeLayer object (with detailed adapted from MapResult)
        # Should have a list of matching shapefiles in place of the `lyr.data_source_path`
        # and `lyr.data_name` properties. (Check implenmentation on this)
        'multiple_matching_files': 'multiple-matching-files',

        # Details to be confirmed
        '_runner.build_project_files': 'project-build-error',

        # A `NameResult` object
        'check_dir': 'name_result'
    }


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
                    nplus_state = step.run(line_printer, **kwargs)
            else:
                logger.info('Starting: {}'.format(step.running_msg))
                nplus_state = step.run(line_printer, **kwargs)

            # Used to increment the state *only* if no new Steps where returned
            n_state = _add_steps_from_state_to_stack(nplus_state, stack, n_state)

        return n_state
    except Exception as exp:
        pass_back = {
            'exp': exp,
            'stack_trace': traceback.format_exc()
        }

        line_printer(logging.ERROR, 'Unable to continue following the previous error', None, **pass_back)
