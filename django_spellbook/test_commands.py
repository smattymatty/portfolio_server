# django_spellbook/tests/test_commands.py

import os
from pathlib import Path
from django.test import TestCase, override_settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.conf import settings
from django_spellbook.management.commands.spellbook_md import Command, ProcessedFile, MarkdownProcessingError


class SpellbookMDCommandTest(TestCase):
    def setUp(self):
        # Create temporary test directories
        self.test_md_path = Path(settings.BASE_DIR) / 'test_md_files'
        self.test_content_app = 'test_content'
        self.test_content_path = Path(
            settings.BASE_DIR) / self.test_content_app

        # Create necessary directories
        self.test_md_path.mkdir(exist_ok=True)
        self.test_content_path.mkdir(exist_ok=True)

        # Create a test markdown file
        self.test_md_file = self.test_md_path / 'test.md'
        self.test_md_file.write_text("# Test\nThis is a test")

        # Initialize command
        self.command = Command()
        self.command.md_file_path = str(self.test_md_path)
        self.command.content_app = self.test_content_app

    def tearDown(self):
        # Clean up test directories
        import shutil
        if self.test_md_path.exists():
            shutil.rmtree(self.test_md_path)
        if self.test_content_path.exists():
            shutil.rmtree(self.test_content_path)

    def test_process_file_valid(self):
        """Test processing a valid markdown file"""
        processed_file = self.command.process_file(
            str(self.test_md_path),
            'test.md',
            []
        )

        self.assertIsInstance(processed_file, ProcessedFile)
        self.assertEqual(processed_file.original_path, self.test_md_file)
        self.assertIn('<h1>Test</h1>', processed_file.html_content)
        self.assertEqual(processed_file.relative_url, 'test')

    def test_process_file_nonexistent(self):
        """Test processing a non-existent file"""
        with self.assertRaises(MarkdownProcessingError):
            self.command.process_file(
                str(self.test_md_path),
                'nonexistent.md',
                []
            )

    def test_process_file_invalid_encoding(self):
        """Test processing a file with invalid encoding"""
        invalid_file = self.test_md_path / 'invalid.md'
        with open(invalid_file, 'wb') as f:
            f.write(b'\x80\x81')

        with self.assertRaises(MarkdownProcessingError):
            self.command.process_file(
                str(self.test_md_path),
                'invalid.md',
                []
            )

    def test_create_template(self):
        """Test template creation"""
        template_path = Path(self.test_content_path) / \
            'templates' / 'test.html'
        html_content = "<h1>Test</h1>"

        self.command.create_template(template_path, html_content)

        self.assertTrue(template_path.exists())
        self.assertEqual(template_path.read_text(), html_content)

    def test_get_folder_list(self):
        """Test folder list generation"""
        test_subfolder = self.test_md_path / 'subfolder'
        test_subfolder.mkdir()

        folder_list = self.command.get_folder_list(str(test_subfolder))

        self.assertEqual(folder_list, ['subfolder'])

    def test_full_command_execution(self):
        """Test full command execution"""
        # Create a more complex test structure
        (self.test_md_path / 'folder1').mkdir()
        (self.test_md_path / 'folder1' / 'test1.md').write_text("# Test 1")
        (self.test_md_path / 'folder2').mkdir()
        (self.test_md_path / 'folder2' / 'test2.md').write_text("# Test 2")

        # Execute command
        call_command('spellbook_md')

        # Check if templates were created
        self.assertTrue((self.test_content_path / 'templates' / self.test_content_app /
                        'spellbook_md' / 'test.html').exists())
        self.assertTrue((self.test_content_path / 'templates' / self.test_content_app /
                        'spellbook_md' / 'folder1' / 'test1.html').exists())
        self.assertTrue((self.test_content_path / 'templates' / self.test_content_app /
                        'spellbook_md' / 'folder2' / 'test2.html').exists())

        # Check if views.py and urls.py were created in django_spellbook
        self.assertTrue(Path(settings.BASE_DIR) /
                        'django_spellbook' / 'views.py')
        self.assertTrue(Path(settings.BASE_DIR) /
                        'django_spellbook' / 'urls.py')

# In tests/test_commands.py


class SpellbookMDBaseTemplateTest(TestCase):
    def setUp(self):
        # Basic setup similar to SpellbookMDCommandTest
        self.test_md_path = Path(settings.BASE_DIR) / 'test_md_files'
        self.test_content_app = 'test_content'
        self.test_content_path = Path(
            settings.BASE_DIR) / self.test_content_app

        self.test_md_path.mkdir(exist_ok=True)
        self.test_content_path.mkdir(exist_ok=True)

        # Create test templates directory
        self.templates_dir = self.test_content_path / 'templates' / self.test_content_app
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Create a base template
        self.base_template = self.templates_dir / 'base.html'
        self.base_template.write_text("""
<!DOCTYPE html>
<html>
<head><title>Spellbook</title></head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
""")

        self.command = Command()
        self.command.md_file_path = str(self.test_md_path)
        self.command.content_app = self.test_content_app

    def tearDown(self):
        import shutil
        if self.test_md_path.exists():
            shutil.rmtree(self.test_md_path)
        if self.test_content_path.exists():
            shutil.rmtree(self.test_content_path)

    @override_settings(SPELLBOOK_MD_BASE_TEMPLATE=f'test_content/base.html')
    def test_create_template_with_base(self):
        """Test template creation with base template"""
        template_path = Path(self.test_content_path) / \
            'templates' / 'test.html'
        html_content = "<h1>Test</h1>"

        self.command.create_template(template_path, html_content)

        created_content = template_path.read_text()
        self.assertIn("{% extends 'test_content/base.html' %}",
                      created_content)
        self.assertIn("{% block spellbook_md %}", created_content)
        self.assertIn("<h1>Test</h1>", created_content)
        self.assertIn("{% endblock %}", created_content)

    def test_create_template_without_base(self):
        """Test template creation without base template"""
        template_path = Path(self.test_content_path) / \
            'templates' / 'test.html'
        html_content = "<h1>Test</h1>"

        self.command.create_template(template_path, html_content)

        created_content = template_path.read_text()
        self.assertNotIn("{% extends", created_content)
        self.assertNotIn("{% block spellbook_md %}", created_content)
        self.assertEqual(created_content, html_content)

    @override_settings(SPELLBOOK_MD_BASE_TEMPLATE='nonexistent/base.html')
    def test_create_template_with_invalid_base(self):
        """Test template creation with invalid base template path"""
        template_path = Path(self.test_content_path) / \
            'templates' / 'test.html'
        html_content = "<h1>Test</h1>"

        # Should still create template even if base template doesn't exist
        # Django will raise TemplateDoesNotExist when rendering if base isn't found
        self.command.create_template(template_path, html_content)

        created_content = template_path.read_text()
        self.assertIn("{% extends 'nonexistent/base.html' %}", created_content)
