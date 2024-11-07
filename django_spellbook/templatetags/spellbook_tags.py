from django import template

register = template.Library()


@register.inclusion_tag('spellbook/toc.html')
def show_toc(markdown_content):
    """Generate table of contents from markdown headers"""
    pass


@register.inclusion_tag('spellbook/metadata.html')
def show_metadata(markdown_file):
    """Display metadata in a formatted way"""
    pass
