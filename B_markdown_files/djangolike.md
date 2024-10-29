Regular markdown text here

{% div .custom-class #unique-id data-test="value" %}
This is inside a div with:

- custom class
- unique ID
- data attribute
  {% enddiv %}

{% section .hero .bg-primary %}

# Hero Section

Some content here with **bold** and _italic_ text
{% endsection %}

{% aside .notes #sidebar role="complementary" %}

> Important note

1. First point
2. Second point
   {% endaside %}

{% article .blog-post #post-1 data-author="john" %}

## Blog Post Title

Regular paragraph with [link](https://example.com)

- List item 1
- List item 2

```code
Some code block
```

{% endarticle %}
