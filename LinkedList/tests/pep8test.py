import pep8

from . import LinkedListTestCase

class LinkedListPep8TestCase(LinkedListTestCase):
    
    def test_style_conformance(self):
        style_guide = pep8.StyleGuide()
        result = style_guide.input_dir("../linkedlist")
        result2 = style_guide.check_files(["../wsgi.py", "../manage.py"])
        self.assertEqual(result.total_errors + result2.total_errors, 0, 
                         "Found errors and/or warnings")
