# import mapactionpy_controller.config_verify as config_verify
import logging


class Step():
    def __init__(self, func, running_msg, complete_msg, fail_msg):
        self.func = func
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
            # long_msg = '{}\n{}'.format(self.fail_msg, exp)
            # pass_back['result'] = str(exp)
            pass_back['exp'] = exp
            set_status(logging.ERROR, self.fail_msg, self, **pass_back)
