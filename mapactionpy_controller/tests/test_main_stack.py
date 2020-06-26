from unittest import TestCase
from mapactionpy_controller.main_stack import process_stack
from mapactionpy_controller.steps import Step


class TestMainStack(TestCase):

    def get_append_to_list(self, step_name):
        def append_to_list(**kwargs):
            state = kwargs['state']
            state.append(step_name)
            return state

        return append_to_list

    def build_example_steps(self, str_list):
        step_list = []
        for step_name in str_list:
            step_list.append(
                Step(
                    self.get_append_to_list(step_name),
                    'DEMO: Doing  {}'.format(step_name),
                    'DEMO: Passed {}'.format(step_name),
                    'DEMO: Failed {}'.format(step_name)
                )
            )

        return step_list

    def setUp(self):
        pass

    def test_simple_step_list(self):
        starter_list = ['AAA', 'BBB', 'CCC', 'DDD']
        starter_steps = self.build_example_steps(starter_list)
        final_state = process_stack(starter_steps, [])

        self.assertEqual(starter_list, final_state)
        print('\nfinal state = {}'.format(final_state))

    def test_add_single_step_into_stack(self):

        def get_inject_steps(**kwargs):
            return self.build_example_steps(['111'])[0]

        starter_list = ['AAA', 'BBB', 'CCC', 'DDD']
        expected_list = ['AAA', 'BBB', '111', 'DDD']

        starter_steps = self.build_example_steps(starter_list)

        # change the func on one of the step, to a function which returns more Step objects
        starter_steps[2].func = get_inject_steps

        final_state = process_stack(starter_steps, [])
        self.assertEqual(final_state, expected_list)
        # print('\nfinal list = {}'.format(final_state))

    def test_add_multiple_steps_into_stack(self):

        def get_inject_steps(**kwargs):
            return self.build_example_steps(['111', '222', '333'])

        starter_list = ['AAA', 'BBB', 'CCC', 'DDD']
        expected_list = ['AAA', 'BBB', '111', '222', '333', 'DDD']

        starter_steps = self.build_example_steps(starter_list)

        # change the func on one of the step, to a function which returns more Step objects
        starter_steps[2].func = get_inject_steps

        final_state = process_stack(starter_steps, [])
        self.assertEqual(final_state, expected_list)
        # print('\nfinal list = {}'.format(final_state))

    def test_non_list_state_object(self):
        pass

    # def test_distinguish_between_falsy_kwargs(self):
    #     inputs = [
    #         None,
    #         True,
    #         False,
    #         [],
    #         ['AAA', 'BBB', 'CCC', 'DDD'],
    #         self.build_example_steps(['111', '222', '333']),
    #         {},
    #         {'item1': 'value1', 'item2': 'value2'}
    #     ]

    #     output = {
    #         0: 'None literal',
    #         1: 'True literal',
    #         2: 'False literal',
    #         3: 'empty list',
    #         4: 'non-empty list',
    #         5: 'step list',
    #         6: 'empty dict',
    #         7: 'non-empty dict',
    #         8: 'recipe',
    #         9: 'other object'
    #     }

    #     for n in range(0, len(inputs)):
    #         print()
    #         print('option[n]={}'.format(inputs[n]))
    #         print('bool(option[n]={})'.format(bool(inputs[n])))
    #         print('is `dict` option[n]={} '.format(isinstance(inputs[n], dict)))
    #         print('is `bool` option[n]={} '.format(isinstance(inputs[n], bool)))
    #         print('is `None` option[n]={} '.format(inputs[n] is None))

    #         self.assertEqual(self.get_my_type(inputs[n]), output[n])

    # def get_my_type(self, obj):
    #     if obj is None:
    #         return 'None literal'
    #         # (list, True): 'step list',
    #         # MapRecipe: 'recipe',
    #         # 9: 'other object'

    #     a = {
    #         (bool, True): 'True literal',
    #         (bool, False): 'False literal',
    #         (list, False): 'empty list',
    #         (list, True): 'non-empty list',
    #         (dict, False): 'empty dict',
    #         (dict, True): 'non-empty dict',
    #     }

    #     try:
    #         return a[type(obj), bool(obj)]
    #     except KeyError:
    #         return 'other object'
