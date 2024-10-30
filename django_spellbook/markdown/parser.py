import markdown

from .extension import DjangoLikeTagExtension, CodeBlockExtension


class MarkdownParser:
    def __init__(self, markdown_text):
        self.markdown_text = markdown_text
        self.html = markdown.markdown(
            self.markdown_text,
            extensions=[DjangoLikeTagExtension(), CodeBlockExtension()],
        )

    def get_html(self):
        return self.html

    def get_markdown(self):
        return self.markdown_text
