import markdown

from .extensions.django_like import DjangoLikeTagExtension
from .extensions.code_block import CodeBlockExtension


class MarkdownParser:
    def __init__(self, markdown_text):
        self.markdown_text = markdown_text
        self.html = markdown.markdown(
            self.markdown_text,
            extensions=[DjangoLikeTagExtension(
            ), 'markdown.extensions.fenced_code'],
        )

    def get_html(self):
        return self.html

    def get_markdown(self):
        return self.markdown_text
