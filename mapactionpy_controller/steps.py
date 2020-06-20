# import mapactionpy_controller.config_verify as config_verify
import logging


class Step():
    def __init__(self, func, running_msg, complete_msg, fail_msg):
        self.func = func
        self.running_msg = running_msg
        self.complete_msg = complete_msg
        self.fail_msg = fail_msg

    def run(self, set_status, verbose, **kwargs):
        try:
            if all(kwargs.values()):
                result = self.func(**kwargs)
            else:
                result = self.func()

            if verbose:
                msg = '{}\n{}'.format(self.complete_msg, result)
            else:
                msg = self.complete_msg

            set_status(logging.INFO, msg, self, **kwargs)
            return result
            # return True
        except Exception as exp:
            fail_msg = '{}\n{}'.format(self.fail_msg, exp)
            set_status(logging.ERROR, fail_msg, self, **kwargs)
            # set_status(logging.DEBUG, traceback.format_exc())
