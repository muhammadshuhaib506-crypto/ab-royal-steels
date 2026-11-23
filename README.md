# AB Royal Steels website

A static, multi-page corporate website. No build step is needed to host it: upload the contents of this folder to any web host (Netlify, Vercel, cPanel, S3, GitHub Pages).

## Pages
- `index.html` Home (3-slide hero)
- `about.html`, `products.html`, `industries.html`, `process.html`, `projects.html`
- `infrastructure.html`, `quality.html`, `leadership.html`, `contact.html`, `quote.html`
- `products/*.html` 29 product detail pages (specifications, size chart, applications, enquiry form)


## Things to fill in
Every piece of information we did not have is shown as a red dashed **[placeholder]** (class `ph`).
Search the HTML for `class="ph"` to find them: phone, email, address, hours, year established,
founder and team, certifications, product grades / sizes / thickness, fleet and facility details, and project entries.
Vision and mission statements are drafts for review.

## Photos
Image areas show generated steel artwork until you add real photos.
1. Put photos in `assets/photos/`.
2. In `assets/js/photos.js`, add `'key': 'assets/photos/file.jpg'`. The key is the `data-key` attribute of the image area
   (e.g. `hero-truck`, `hero-sheets`, `hero-pipes`, `cat-sheets`, `cat-pipes`, `cat-sections`, `cat-iron`, `p-ms-pipes`, `p-gi-sheets` ...).

## Forms
Forms validate in the browser. To receive enquiries, paste a form endpoint (Formspree, Getform, Basin or your own server)
into `FORM_ENDPOINT` at the top of `assets/js/site.js`.

## Logo files
`assets/img/logo-white.svg` (for red / navy / dark backgrounds), `logo-color.svg` (for white), `mark-white.svg`, `mark-red.svg`, and `truck.png` (cut-out of the branded truck).

## Editing at scale
The pages are generated from `source/build.py` and `source/data.py` (product names, descriptions, applications, industries, process steps).
Edit those and run `python3 source/build.py` to regenerate all pages, or edit the HTML directly.
