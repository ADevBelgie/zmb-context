import unittest
import os
import shutil
import tempfile
from zmb.context_architect.cursor_rules import detect_project_type, generate_cursor_rules_content

class TestCursorRules(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_file(self, filename):
        path = os.path.join(self.test_dir, filename)
        with open(path, 'w') as f:
            f.write('')
        return path

    def test_detect_python(self):
        self.create_file('requirements.txt')
        types = detect_project_type(self.test_dir)
        self.assertIn('python', types)

    def test_detect_django(self):
        self.create_file('manage.py')
        types = detect_project_type(self.test_dir)
        self.assertIn('django', types)

    def test_detect_node(self):
        self.create_file('package.json')
        types = detect_project_type(self.test_dir)
        self.assertIn('node', types)

    def test_detect_nextjs(self):
        self.create_file('next.config.js')
        types = detect_project_type(self.test_dir)
        self.assertIn('nextjs', types)

    def test_content_generation(self):
        content = generate_cursor_rules_content(['python', 'django'])
        self.assertIn('## Python', content)
        self.assertIn('## Django', content)
        self.assertNotIn('## Node/JavaScript', content)

if __name__ == '__main__':
    unittest.main()
