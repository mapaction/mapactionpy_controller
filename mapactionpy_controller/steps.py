# import mapactionpy_controller.config_verify as config_verify
import logging
import traceback


class Step():
    """
    This represents the atomic "unit of work" within the map production automation.

    :param func:
        * Must accept a **kwargs param. If there is a state object this is passed as `kwargs['state']`
        * If the function completes successfully it should return the updated state object. This should be
          "bare" (ie not wrapped in a dict ala kwargs)
        * If the function does not complete successfully it should raise an exception.
    :param fail_threshold: Expresses the severity with which an exception from `func` should be treated. In
        any case the exception will be handled and a JIRA tasks logged as appropriate.
        * If = `logging.ERROR` - the exception will terminate the program.
        * If = `logging.WARNING` - the exception will not result in termination. A JRIA task will be logged the
          program will attempt to continue, though the results may not be want the user intended.
    :param running_msg:
    :param complete_msg:
    :param fail_msg:
    :returns:
    """

    def __init__(self, func, fail_threshold, running_msg, complete_msg, fail_msg):
        self.func = func
        self.fail_threshold = fail_threshold
        self.running_msg = running_msg
        self.complete_msg = complete_msg
        self.fail_msg = fail_msg

    def run(self, set_status, **kwargs):
        pass_back = kwargs.copy()

        try:
            result = self.func(**kwargs)
            # long_msg = '{}\n{}'.format(self.complete_msg, result)
            pass_back['result'] = result
            set_status(logging.INFO, self.complete_msg, self, **pass_back)
            return result
        except Exception as exp:
            pass_back['exp'] = exp
            pass_back['stack_trace'] = traceback.format_exc()
            set_status(self.fail_threshold, self.fail_msg, self, **pass_back)
            # set_status(logging.ERROR, self.fail_msg, self, **pass_back)

            # Do we want to raise an ERROR or a WARNING?
            if self.fail_threshold >= logging.ERROR:
                raise exp

            # If this is just a warning then we return the unaltered state object
            # TODO Review is it is possible in the case of warnings, to pass back an updated
            # state as an args to the relevant Exception.
            return kwargs.get('state', None)
