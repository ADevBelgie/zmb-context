import unittest
import os
import shutil
import tempfile
from zmb.context_architect.analyzer import DependencyAnalyzer

class TestDependencyAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.analyzer = DependencyAnalyzer(self.test_dir)

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def create_file(self, path, content):
        full_path = os.path.join(self.test_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return full_path

    def test_python_absolute_import(self):
        # Create a dummy package structure
        self.create_file('pkg/__init__.py', '')
        target = self.create_file('pkg/module.py', 'def foo(): pass')
        
        source = self.create_file('main.py', 'import pkg.module')
        
        # Re-initialize analyzer to pick up new files in file_map
        self.analyzer = DependencyAnalyzer(self.test_dir)
        
        deps = self.analyzer.get_dependencies(source)
        self.assertIn(os.path.normpath(target), deps)

    def test_python_from_import(self):
        self.create_file('utils.py', 'def helper(): pass')
        source = self.create_file('app.py', 'from utils import helper')
        
        self.analyzer = DependencyAnalyzer(self.test_dir)
        deps = self.analyzer.get_dependencies(source)
        
        expected = os.path.join(self.test_dir, 'utils.py')
        self.assertIn(os.path.normpath(expected), deps)

    def test_js_relative_import(self):
        target = self.create_file('components/Button.jsx', 'export default () => {}')
        source = self.create_file('App.jsx', "import Button from './components/Button'")
        
        self.analyzer = DependencyAnalyzer(self.test_dir)
        deps = self.analyzer.get_dependencies(source)
        
        self.assertIn(os.path.normpath(target), deps)

    def test_js_require(self):
        target = self.create_file('lib/api.js', 'module.exports = {}')
        source = self.create_file('server.js', "const api = require('./lib/api')")
        
        self.analyzer = DependencyAnalyzer(self.test_dir)
        deps = self.analyzer.get_dependencies(source)
        
        self.assertIn(os.path.normpath(target), deps)

if __name__ == '__main__':
    unittest.main()
