# import mapactionpy_controller.config_verify as config_verify
import logging
import traceback


class Step():
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
            return kwargs.get('state', None)
