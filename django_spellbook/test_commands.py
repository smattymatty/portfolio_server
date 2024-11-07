# django_spellbook/tests/test_commands.py

import shutil
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
        # Create necessary directories for templates
        template_dir = self.test_content_path / 'templates' / \
            self.test_content_app / 'spellbook_md'
        template_dir.mkdir(parents=True, exist_ok=True)

        # Set up the command's template directory
        self.command.template_dir = str(template_dir)

        processed_file = self.command.process_file(
            str(self.test_md_path),
            'test.md',
            []
        )

        self.assertIsInstance(processed_file, ProcessedFile)
        self.assertEqual(processed_file.original_path, self.test_md_file)
        # Use assertIn for more flexible HTML comparison
        self.assertIn('<h1>Test</h1>', processed_file.html_content.strip())
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

    @override_settings(SPELLBOOK_MD_BASE_TEMPLATE=None)
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
        # Create necessary directories
        template_dir = self.test_content_path / 'templates' / \
            self.test_content_app / 'spellbook_md'
        template_dir.mkdir(parents=True, exist_ok=True)

        # Create a more complex test structure
        folder1 = self.test_md_path / 'folder1'
        folder2 = self.test_md_path / 'folder2'
        folder1.mkdir(exist_ok=True)
        folder2.mkdir(exist_ok=True)

        # Create test markdown files
        (folder1 / 'test1.md').write_text("# Test 1")
        (folder2 / 'test2.md').write_text("# Test 2")

        # Set up required settings
        with self.settings(
            SPELLBOOK_MD_PATH=str(self.test_md_path),
            SPELLBOOK_CONTENT_APP=self.test_content_app
        ):
            # Execute command
            call_command('spellbook_md')

            # Check if templates were created
            self.assertTrue((template_dir / 'test.html').exists())
            self.assertTrue((template_dir / 'folder1' / 'test1.html').exists())
            self.assertTrue((template_dir / 'folder2' / 'test2.html').exists())

            # Check if views.py and urls.py were created
            self.assertTrue((self.test_content_path / 'views.py').exists())
            self.assertTrue((self.test_content_path / 'urls.py').exists())


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

    @override_settings(SPELLBOOK_MD_BASE_TEMPLATE='test_content/base.html')
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

    # Explicitly set to None
    @override_settings(SPELLBOOK_MD_BASE_TEMPLATE=None)
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


# tests/test_documentation.py


class DocumentationClaimsTest(TestCase):
    """Tests that verify all functionality claimed in the documentation"""

    def setUp(self):
        # Create test directories
        self.test_md_path = Path(settings.BASE_DIR) / 'test_md_files'
        self.test_content_app = 'test_content'
        self.test_content_path = Path(
            settings.BASE_DIR) / self.test_content_app

        # Create necessary directories
        self.test_md_path.mkdir(exist_ok=True)
        self.test_content_path.mkdir(exist_ok=True)

        # Create templates directory
        self.templates_dir = self.test_content_path / 'templates' / self.test_content_app
        self.templates_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        # Clean up test directories
        if self.test_md_path.exists():
            shutil.rmtree(self.test_md_path)
        if self.test_content_path.exists():
            shutil.rmtree(self.test_content_path)

    def test_basic_markdown_parsing(self):
        """Test that basic markdown parsing works"""
        md_content = "# Test Heading\nThis is a test paragraph."
        md_file = self.test_md_path / 'basic.md'
        md_file.write_text(md_content)

        call_command('spellbook_md')

        template_path = self.templates_dir / 'spellbook_md' / 'basic.html'
        self.assertTrue(template_path.exists())
        content = template_path.read_text()
        self.assertIn('<h1>Test Heading</h1>', content)
        self.assertIn('<p>This is a test paragraph.</p>', content)

    def test_custom_div_with_class_and_id(self):
        """Test the custom div tag with class and ID as shown in documentation"""
        md_content = """{% div .my-class #my-id %}
This is a custom div block with a class and an ID.
{% enddiv %}"""

        md_file = self.test_md_path / 'custom_div.md'
        md_file.write_text(md_content)

        call_command('spellbook_md')

        template_path = self.templates_dir / 'spellbook_md' / 'custom_div.html'
        self.assertTrue(template_path.exists())
        content = template_path.read_text()
        self.assertIn('<div class="my-class" id="my-id">', content)

    def test_htmx_attributes(self):
        """Test HTMX attributes support as claimed in documentation"""
        md_content = """{% button .my-class #my-id hx-get="/api/get-data" hx-swap="outerHTML" %}
Click me
{% endbutton %}"""

        md_file = self.test_md_path / 'htmx.md'
        md_file.write_text(md_content)

        call_command('spellbook_md')

        template_path = self.templates_dir / 'spellbook_md' / 'htmx.html'
        self.assertTrue(template_path.exists())
        content = template_path.read_text()
        self.assertIn('hx-get="/api/get-data"', content)
        self.assertIn('hx-swap="outerHTML"', content)

    @override_settings(SPELLBOOK_MD_BASE_TEMPLATE='test_content/base.html')
    def test_base_template_integration(self):
        """Test base template integration"""
        # Create base template
        base_template = self.templates_dir / 'base.html'
        base_template.write_text("""
{% block spellbook_md %}
{% endblock %}
        """)

        md_content = "# Test Content"
        md_file = self.test_md_path / 'with_base.md'
        md_file.write_text(md_content)

        call_command('spellbook_md')

        template_path = self.templates_dir / 'spellbook_md' / 'with_base.html'
        self.assertTrue(template_path.exists())
        content = template_path.read_text()
        self.assertIn("{% extends 'test_content/base.html' %}", content)
        self.assertIn("{% block spellbook_md %}", content)

    def test_nested_directory_structure(self):
        """Test handling of nested directory structure"""
        # Create nested structure as mentioned in docs
        (self.test_md_path / 'articles').mkdir()
        md_file = self.test_md_path / 'articles' / 'guide.md'
        md_file.write_text("# Guide\nThis is a guide.")

        call_command('spellbook_md')

        # Check if template was created with correct structure
        template_path = self.templates_dir / 'spellbook_md' / 'articles' / 'guide.html'
        self.assertTrue(template_path.exists())

        # Check if URL pattern was generated correctly
        urls_file = Path(settings.BASE_DIR) / 'django_spellbook' / 'urls.py'
        self.assertTrue(urls_file.exists())
        urls_content = urls_file.read_text()
        self.assertIn("'articles/guide'", urls_content)

    def test_view_generation(self):
        """Test that views are generated correctly"""
        md_file = self.test_md_path / 'test_view.md'
        md_file.write_text("# Test View")

        call_command('spellbook_md')

        views_file = Path(settings.BASE_DIR) / 'django_spellbook' / 'views.py'
        self.assertTrue(views_file.exists())
        views_content = views_file.read_text()
        self.assertIn('def view_test_view', views_content)
        self.assertIn('return render', views_content)

    def test_url_generation(self):
        """Test that URLs are generated correctly"""
        md_file = self.test_md_path / 'test_url.md'
        md_file.write_text("# Test URL")

        call_command('spellbook_md')

        urls_file = Path(settings.BASE_DIR) / 'django_spellbook' / 'urls.py'
        self.assertTrue(urls_file.exists())
        urls_content = urls_file.read_text()
        self.assertIn('urlpatterns = [', urls_content)
        self.assertIn("path('test_url'", urls_content)
