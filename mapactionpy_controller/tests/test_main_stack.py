from unittest import TestCase
from mapactionpy_controller.main_stack import process_stack
from mapactionpy_controller.steps import Step


class TestMainStack(TestCase):

    def get_append_state(self, step_name, state_obj_type):
        def append_to_list(**kwargs):
            state = kwargs['state']
            state.append(step_name)
            return state

        def append_to_dict(**kwargs):
            state = kwargs['state']
            state[step_name] = step_name
            return state

        def append_to_string(**kwargs):
            state = kwargs['state']
            state = state + step_name
            return state

        func_dict = {
            'list': append_to_list,
            'dict': append_to_dict,
            'string': append_to_string
        }

        return func_dict[state_obj_type]

    def build_example_steps(self, str_list, state_obj_type):
        step_list = []
        for step_name in str_list:
            step_list.append(
                Step(
                    self.get_append_state(step_name, state_obj_type),
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

        test_cases = [
            ('list', [], ['AAA', 'BBB', 'CCC', 'DDD']),
            ('dict', {}, {'AAA': 'AAA', 'BBB': 'BBB', 'CCC': 'CCC', 'DDD': 'DDD'}),
            ('string', '', 'AAABBBCCCDDD')
        ]

        for state_type, initial_state, expected_state in test_cases:
            starter_steps = self.build_example_steps(starter_list, state_type)
            final_state = process_stack(starter_steps, initial_state)
            self.assertEqual(expected_state, final_state)
            print('\nfinal state = {}'.format(final_state))

    def test_add_single_step_into_stack(self):

        starter_list = ['AAA', 'BBB', 'CCC', 'DDD']

        test_cases = [
            ('list', [], ['AAA', 'BBB', '111', 'DDD']),
            ('dict', {}, {'AAA': 'AAA', 'BBB': 'BBB', '111': '111', 'DDD': 'DDD'}),
            ('string', '', 'AAABBB111DDD')
        ]

        for state_type, initial_state, expected_state in test_cases:
            def get_inject_steps(**kwargs):
                return self.build_example_steps(['111'], state_type)[0]

            starter_steps = self.build_example_steps(starter_list, state_type)
            # change the func on one of the step, to a function which returns more Step objects
            starter_steps[2].func = get_inject_steps
            final_state = process_stack(starter_steps, initial_state)
            self.assertEqual(expected_state, final_state)
            print('\nfinal list = {}'.format(final_state))

    def test_add_multiple_steps_into_stack(self):

        starter_list = ['AAA', 'BBB', 'CCC', 'DDD']

        test_cases = [
            ('list', [], ['AAA', 'BBB', '111', '222', '333', 'DDD']),
            ('dict', {}, {'AAA': 'AAA', 'BBB': 'BBB', '111': '111', '222': '222', '333': '333', 'DDD': 'DDD'}),
            ('string', '', 'AAABBB111222333DDD')
        ]

        for state_type, initial_state, expected_state in test_cases:
            def get_inject_steps(**kwargs):
                return self.build_example_steps(['111', '222', '333'], state_type)

            starter_steps = self.build_example_steps(starter_list, state_type)
            # change the func on one of the step, to a function which returns more Step objects
            starter_steps[2].func = get_inject_steps
            final_state = process_stack(starter_steps, initial_state)
            self.assertEqual(expected_state, final_state)
            print('\nfinal list = {}'.format(final_state))

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
