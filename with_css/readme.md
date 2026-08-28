# Workshop 2: Website (HTML + CSS)

**Course:** Web Applications — Semester II 2026
**Student:** Ismael Paredes
**Professor:** Francisco Hidrobo

## Objective

Add CSS to the website built in Workshop 1 to improve layout and presentation, without changing its core content.

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
├── images/
│   ├── profile-photo.jpg
│   ├── simba-the-cat.jpg
│   └── comsoc.JPG
└── css/
    ├── base.css     → variables, reset, typography, .card component
    ├── nav.css       → header and navigation
    ├── forms.css     → contact form
    └── tables.css    → schedule table with color-coded courses
```

## How to View

Open `my-site/index.html` directly in a browser, or serve it locally with:

```bash
cd my-site
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Stylesheets

- **base.css** — CSS custom properties for color palette and spacing, a box-sizing reset, base typography, and a reusable `.card` component used across all pages.
- **nav.css** — Flexbox navigation with a sticky header and an `.active` class marking the current page.
- **forms.css** — Styling for the contact form (layout, inputs, focus states, submit button).
- **tables.css** — Weekly schedule table with black borders and one background color per course.
