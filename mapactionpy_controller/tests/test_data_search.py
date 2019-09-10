from unittest import TestCase
import mapactionpy_controller.data_search as data_search
import sys
import os
import six
import StringIO

# works differently for python 2.7 and python 3.x
if six.PY2:
    import mock  # noqa: F401
    from mock import mock_open, patch
else:
    from unittest import mock  # noqa: F401
    from unittest.mock import mock_open, patch  # noqa: F401


class TestDataSearch(TestCase):

    def setUp(self):
        parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.cmf_descriptor_path = os.path.join(
            parent_dir, 'example', 'cmf_description_flat_test.json')
        self.recipe_file = os.path.join(parent_dir, 'example', 'product_bundle_example.json')
        self.non_existant_file = os.path.join(parent_dir, 'example', 'non-existant-file.json')
        self.output_file = os.path.join(parent_dir, 'example', 'delete-me-test-output-file.json')

        # self.ds = data_search.DataSearch(cmf_descriptor_path)

    def test_args(self):
        sys.argv[1:] = ['--cmf', self.cmf_descriptor_path,
                        '--recipe-file', self.recipe_file,
                        '--output-file', 'somefile']
        args = data_search.get_args()
        self.assertEquals(self.cmf_descriptor_path, args.crash_move_folder)
        self.assertEquals(self.recipe_file, args.recipe_file)
        self.assertEquals('somefile', args.output_file)

    def test_non_existant_files_args(self):
        sys.argv[1:] = ['--cmf', self.cmf_descriptor_path,
                        '--recipe-file', self.non_existant_file]

        with self.assertRaises(SystemExit):
            data_search.get_args()
        
    @mock.patch('json.dump')
    @mock.patch('builtins.open', new_callable=mock_open())
    def test_data_search_main(self, m, m_json):
        sys.argv[1:] = ['--cmf', self.cmf_descriptor_path,
                        '--recipe-file', self.recipe_file,
                        '--output-file', self.output_file]

        dummy_file = StringIO.StringIO()

        m.return_value = dummy_file
        data_search.main()
        print(dummy_file.getvalue())

        # m.assert_called_once_with(self.output_file, 'w')
        # In this case we don't expect the data serach to find anything, therefore the recipe
        # should be returned unchanged.
        handle = m()
        m.write.assert_called_once_with('self.recipe_file')
        # handle.write.assert_called_once_with('self.recipe_file')


        #outfile = StringIO.StringIO()

        #with self.assertRaises(SystemExit):


        # with patch('builtins.open', new_callable=mock_open()) as m:
        #     with patch('json.dump') as m_json:
        #         self.mc.save_data_to_file(self.data)


        #         # simple assertion that your open was called
        #         m.assert_called_with('/tmp/data.json', 'w')

        #         # assert that you called m_json with your data
        #         m_json.assert_called_with(self.data, m.return_value)

        # sys.argv[1:] = ['-v']
        # with self.assertRaises(SystemExit):
        #     data_search.get_args()
