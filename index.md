---
layout: clean-layout
---

#  שאמבאלה אתר גיבוי

## יומן השיעורים

{: #lessons }

<ul>
  {% for post3 in site.posts %}
   {% if post3.path contains 'lessons_diary' %}
    <li>
      <a href="{{site.baseurl | append:  post3.url }}">{{ post3.title }}</a>
    </li>
   {% endif %}
  {% endfor %}
</ul>
