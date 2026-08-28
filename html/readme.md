# Workshop 1: Website (only HTML)

**Course:** Web Applications — Semester II 2026
**Student:** Ismael Paredes
**Professor:** Francisco Hidrobo

## Objective

Build a multi-page website using only HTML5: semantic elements, lists, a table with `rowspan`, and a form with multiple input types. No CSS involved in this deliverable.

## Environment

- **Web server:** Apache (via XAMPP)
- **Local domain:** `workshop1.webapp` → `127.0.0.1`, mapped via the `hosts` file and served through a virtual host pointing to `my-site/` as the document root.

## Project Structure

```
my-site/
├── index.html
├── pages/
│   ├── courses.html
│   ├── schedule.html
│   ├── contact.html
│   ├── hobbies.html
│   └── clubs.html
└── images/
    ├── profile-photo.jpg
    ├── simba-the-cat.jpg
    └── comsoc.JPG
```

## Pages

- **index.html** — Home page with semantic sectioning (`header`, `nav`, `main`, `section`, `article`, `footer`), student info, profile photo, and a list of academic interests. The `nav` menu is reused across every page.
- **pages/courses.html** — One `article` per course (Distributed Systems, Machine Learning, Cryptography, Web Applications), each with instructor, an ordered list of main topics, an unordered list of expected learnings, and an external link (`target="_blank"`).
- **pages/schedule.html** — Weekly schedule as an HTML `table`, using `rowspan` for courses spanning consecutive hours.
- **pages/contact.html** — Form (no backend) covering `text`, `email`, `date`, `select`, `textarea`, `checkbox`, and `submit`, each input tied to a `label` via `for`/`id`.
- **pages/hobbies.html** — Personal interests organized into categories: cybersecurity practice, music theory, open source.
- **pages/clubs.html** — IEEE ComSoc Yachay Tech Student Branch and the Course Assistant role for Computer Networks.

## How to View

Open `my-site/index.html` directly in a browser, or configure a local Apache virtual host as described above.
