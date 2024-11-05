# Full Stack Development

Creating beautiful, functional, and accessible user interfaces paired with robust web applications requires a carefully chosen tech stack.

My go-to tech stack has changed over the years as I've learned more about web development, as as new tools came and old tools went.

Here's an overview of the key technologies that make modern web development powerful and efficient.

# Back End Development

## Django

Django stands out as a high-level Python web framework that encourages rapid development and clean, pragmatic design. Its built-in admin interface, ORM, and authentication system significantly reduce development time while maintaining security and scalability.

It's open source community, easy to understand documentation, and vast supply of tutorials makes it a great option for back end development.

Key strengths:

- Automatic admin interface generation
- Robust security features out of the box
- Highly scalable with built-in caching support
- Extensive middleware system for request/response processing

TODO: Link to Django Spellbook Open Source Library
TODO: Django 5 by example blog posts

```python
# Example of Django's powerful ORM
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    published = models.DateField()

    def get_related_books(self):
        return Book.objects.filter(author=self.author).exclude(id=self.id)
```

## DigitalOcean

DigitalOcean provides a robust cloud infrastructure that simplifies deployment and scaling. Their App Platform offers:

- Automated deployments from Git
- Built-in SSL certificate management
- Automatic horizontal scaling
- Container registry and Kubernetes support

One of my favorite features of DigitalOcean is their automated deployments from Git I've been using GitHub actions for a while, so this pairs perfectly with my workflow. I also love how easy it is to manage multiple domains, and `.env` variables, making it easy to test in my own environment, and then deploy to production without having to worry about configuration.

## Linux

The backbone of modern web hosting, Linux provides:

- Superior process management with systemd
- Efficient resource utilization
- Robust containerization support
- Comprehensive logging and monitoring

I started using Linux in 2019 because of easier access to Docker and Gunicorn, and because I wanted more contol over my system's resources in order to properly test and deploy my web applications. I love how customizable Linux is, and it's great open source community that provides a lot of great tools that are often on par with, or better than, commercial offerings. Plus, I'm a huge fan of the Linux philosophy of "Do one thing and do it well", and I think it's a great way to build a solid foundation for your web development projects.

# Front End Development

## HTMX

HTMX extends HTML's capabilities to create dynamic interfaces without complex JavaScript frameworks. It excels at:

- Ajax requests directly from HTML
- WebSocket integration
- Server-Sent Events
- Dynamic page updates

```html
<!-- Dynamic content loading with HTMX -->
<div hx-get="/api/latest-posts" hx-trigger="every 2s" hx-swap="innerHTML">
  <!-- Content updates every 2 seconds -->
</div>
```

The way it meshes with the original simplicity of HTML's original design is a game changer. Instead of overly complex JavaScript frameworks, HTMX allows you to create dynamic interfaces without the need for JavaScript. I still like using Vanilla JavaScript for more complex interactions, but HTMX is a great tool for creating simple, dynamic interfaces without the overhead of a full JavaScript framework.

## CSS and HTML

Modern CSS provides powerful features for creating responsive, accessible interfaces:

- CSS Grid for complex layouts
- Custom Properties for theming
- Container Queries for component-based design
- Logical Properties for international layouts

```css
/* Modern CSS example */
.component {
  container-type: inline-size;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: clamp(1rem, 5vw, 2rem);
}
```

My introduction to CSS was through Tailwind, which is a utility-first CSS framework that provides a lot of the same features as Bootstrap, but with a much smaller footprint.

Lately I find myself using vanilla CSS more and more, now that I have learned more about the language and its capabilities, I enjoy the freedom of creating my own classes and the pseudoselectors to go along with them.

## JavaScript

JavaScript enables complex client-side interactions while maintaining accessibility:

- Async/await for clean asynchronous code
- Web Components for reusable elements
- Intersection Observer for performance
- Service Workers for offline capability

```javascript
// Modern JavaScript example
class CustomElement extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  connectedCallback() {
    this.render();
  }
}
```

TODO: Link to Melvor Mod Contest
TODO: Simple Arcade Games

---

This tech stack combines to create web applications that are:

- Highly performant
- Accessible by default
- Easy to maintain
- Scalable for growth
