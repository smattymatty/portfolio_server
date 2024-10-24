import markdown

from .extension import DjangoLikeTagExtension


class MarkdownParser:
    def __init__(self, markdown_text):
        self.markdown_text = markdown_text
        self.html = markdown.markdown(
            self.markdown_text,
            extensions=[DjangoLikeTagExtension()]
        )

    def get_html(self):
        return self.html

    def get_markdown(self):
        return self.markdown_text
