import os

from typing import List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template.loader import render_to_string

from django_spellbook.markdown.parser import MarkdownParser


@dataclass
class ProcessedFile:
    """Represents a processed markdown file"""
    original_path: Path
    html_content: str
    template_path: Path
    relative_url: str


class MarkdownProcessingError(Exception):
    """Custom exception for markdown processing errors"""
    pass


class Command(BaseCommand):
    md_file_path = settings.SPELLBOOK_MD_PATH
    content_app = settings.SPELLBOOK_CONTENT_APP
    content_dir_path = ""
    template_dir = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.md_file_path = settings.SPELLBOOK_MD_PATH
        self.content_app = settings.SPELLBOOK_CONTENT_APP
        self.content_dir_path = ""
        self.template_dir = ""

    help = "Converts markdown to html, with a spellbook twist"

    def handle(self, *args, **options):
        w = os.walk(self.md_file_path)
        processed_files: List[ProcessedFile] = []
        for (dirpath, dirnames, filenames) in w:
            if not self.content_dir_path:
                self.get_content_dir_path(dirpath)
            print(f"Processing {dirpath}")
            print(f"dirnames: {dirnames}")
            print(f"filenames: {filenames}")
            for filename in filenames:
                if filename.endswith(".md"):
                    folder_list = self.get_folder_list(dirpath)
                    processed_file = self.process_file(
                        dirpath, filename, folder_list)
                    if processed_file:  # Only append if processing was successful
                        processed_files.append(processed_file)

                        # Create the template file
                        self.create_template(
                            processed_file.template_path,
                            processed_file.html_content
                        )

        if processed_files:
            self.generate_urls_and_views(processed_files)
            self.stdout.write(self.style.SUCCESS(
                f"Processed {len(processed_files)} markdown files and generated URLs and views"
            ))
        else:
            raise CommandError("No markdown files found")

    def process_file(self, dirpath: str, filename: str, folders: List[str]) -> Optional[ProcessedFile]:
        """
        Process a single markdown file and return its processed details

        Args:
            dirpath: Directory path containing the markdown file
            filename: Name of the markdown file
            folders: List of folder names for template organization

        Returns:
            ProcessedFile object containing processing results

        Raises:
            MarkdownProcessingError: If there's an error processing the file
        """
        try:
            file_path = Path(dirpath) / filename

            # Validate file exists and is markdown
            if not file_path.exists():
                raise MarkdownProcessingError(f"File not found: {file_path}")
            if not filename.endswith('.md'):
                raise MarkdownProcessingError(
                    f"Not a markdown file: {filename}")

            # Read and parse markdown
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_text = f.read()
            except UnicodeDecodeError:
                raise MarkdownProcessingError(
                    f"File encoding error: {file_path}")
            except IOError as e:
                raise MarkdownProcessingError(
                    f"Error reading file {file_path}: {str(e)}")

            # Parse markdown
            try:
                parser = MarkdownParser(md_text)
                html_content = parser.get_html()
            except Exception as e:
                raise MarkdownProcessingError(
                    f"Markdown parsing error: {str(e)}")

            # Calculate paths
            relative_path = file_path.relative_to(Path(self.md_file_path))
            template_path = self.get_template_path(filename, folders)
            relative_url = str(relative_path.with_suffix('')
                               ).replace('\\', '/')

            return ProcessedFile(
                original_path=file_path,
                html_content=html_content,
                template_path=template_path,
                relative_url=relative_url
            )

        except MarkdownProcessingError:
            raise
        except Exception as e:
            raise MarkdownProcessingError(
                f"Unexpected error processing {filename}: {str(e)}")

    def get_template_path(self, filename: str, folders: List[str]) -> Path:
        """Calculate the template path for a processed file"""
        folder_string = ""
        for folder in reversed(folders):
            folder_string = Path(folder_string) / folder

        return Path(self.template_dir) / folder_string / filename.replace('.md', '.html')

    def create_template(self, template_path: Path, html_content: str):
        """
        Create a template file with the processed HTML content.
        If SPELLBOOK_MD_BASE_TEMPLATE is set, wraps the content in template inheritance tags.

        Args:
            template_path: Path where the template should be created
            html_content: The processed HTML content to write
        """
        try:
            # Create directory if it doesn't exist
            template_path.parent.mkdir(parents=True, exist_ok=True)

            # Check for base template setting
            base_template = getattr(
                settings, 'SPELLBOOK_MD_BASE_TEMPLATE', None)

            # Only wrap content if base_template is explicitly set
            if base_template:
                if not base_template.endswith('.html'):
                    base_template += '.html'
                # Wrap content in template inheritance
                final_content = (
                    "{{% extends '{}' %}}\n\n"
                    "{{% block spellbook_md %}}\n"
                    "{}\n"
                    "{{% endblock %}}"
                ).format(base_template, html_content)
            else:
                final_content = html_content

            # Write the template file
            template_path.write_text(final_content)
        except Exception as e:
            raise CommandError(
                f"Could not create template {template_path}\n {e}")

    def get_content_dir_path(self, dirpath):
        try:
            base_path = "/".join(dirpath.split("/")[:-1])
            if not os.path.exists(os.path.join(base_path, self.content_app)):
                raise CommandError(
                    f"Content app {self.content_app} not found in {base_path}"
                )
            self.content_dir_path = os.path.join(
                base_path, self.content_app)
            self.get_or_create_content_app_template_dir()
        except:
            raise CommandError(
                f"Could not create content dir path {self.content_dir_path}"
            )

    def get_or_create_content_app_template_dir(self):
        try:
            base_template_dir = os.path.join(
                self.content_dir_path, f"templates/{self.content_app}/spellbook_md")
            if not os.path.exists(base_template_dir):
                os.makedirs(base_template_dir)
            self.template_dir = base_template_dir
        except Exception as e:
            raise CommandError(
                f"Could not create content app template dir {self.template_dir}\n {e}"
            )

    def get_folder_list(self, dirpath):
        print(f"get_folder_list: {dirpath}")
        folder_split = dirpath.split("/")
        print(f"folder_split: {folder_split}")
        folder_list = []
        # trackers
        done = False
        n = -1
        while not done:
            dirname = folder_split[n]
            print(f"dirname: {dirname}")
            if dirname == str(self.md_file_path).split("/")[-1]:
                done = True
                break
            else:
                folder_list.append(dirname)
                n -= 1
        print(f"folder_list: {folder_list}")
        return folder_list

    def generate_urls_and_views(self, processed_files: List[ProcessedFile]):
        print(processed_files)
        urls = []
        views = []

        for processed_file in processed_files:
            print(f"Processing {processed_file}")

            # We can now directly use the relative_url from ProcessedFile
            url_pattern = processed_file.relative_url
            view_name = f"view_{url_pattern.replace('/', '_').replace('.', '_')}"

            # Get template path relative to the templates directory
            template_path = os.path.join(
                self.content_app, 'spellbook_md', url_pattern + '.html')

            urls.append(
                f"path('{url_pattern}', views.{view_name}, name='{view_name}')")
            views.append(self.generate_view_function(view_name, template_path))

        self.write_urls(urls)
        self.write_views(views)

    def generate_view_function(self, view_name, template_path):
        return f"""
def {view_name}(request):
    return render(request, '{template_path}')
    """

    def write_urls(self, urls):
        try:
            # Write to django_spellbook/urls.py
            spellbook_urls_path = os.path.join(
                os.path.dirname(__file__),
                '../..',
                'urls.py'
            )

            content = """from django.urls import path
from . import views

urlpatterns = [
    {}
]""".format(',\n    '.join(urls))

            with open(spellbook_urls_path, 'w') as f:
                f.write(content)

        except Exception as e:
            raise CommandError(f"Failed to write URLs file: {str(e)}")

    def write_views(self, views):
        try:
            # Write to django_spellbook/views.py
            spellbook_views_path = os.path.join(
                os.path.dirname(__file__),
                '../..',
                'views.py'
            )

            content = """from django.shortcuts import render

{}""".format('\n'.join(views))

            with open(spellbook_views_path, 'w') as f:
                f.write(content)

        except Exception as e:
            raise CommandError(f"Failed to write views file: {str(e)}")

    def get_content_dir_path(self, dirpath):
        try:
            base_path = "/".join(dirpath.split("/")[:-1])
            content_app_path = os.path.join(base_path, self.content_app)
            if not os.path.exists(content_app_path):
                raise CommandError(
                    f"Content app {self.content_app} not found in {base_path}"
                )
            self.content_dir_path = content_app_path
            self.get_or_create_content_app_template_dir()
            self.ensure_urls_views_files()
        except Exception as e:
            raise CommandError(
                f"Could not set up content dir path: {str(e)}"
            )

    def ensure_urls_views_files(self):
        self.urls_file_path = os.path.join(self.content_dir_path, 'urls.py')
        self.views_file_path = os.path.join(self.content_dir_path, 'views.py')

        for file_path in [self.urls_file_path, self.views_file_path]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write("from django.urls import path\n\nurlpatterns = []")
                print(f"Created new file: {file_path}")
