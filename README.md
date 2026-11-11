# TR-103 Industrial Training Daily Diary — Savreet Kaur

A static website documenting a 4-week industrial training in **Data Analytics**
at **World With Web**, built to match the TR-102 diary site.

- **Name:** Savreet Kaur
- **URN:** 2302668
- **College:** Guru Nanak Dev Engineering College, Ludhiana
- **Department:** Computer Science & Engineering
- **Period:** 15 June 2026 – 15 July 2026 (4 weeks × 5 days = 20 working days)
- **Certificate:** Data Analytics, 4 Weeks · issued 23 July 2026 · Sr. No. w03408

---

## Status before publishing

| # | What | Where | Status |
|---|---|---|---|
| 1 | Company logo | `worldwithweb-logo.png` | done |
| 2 | Training confirmation letter | `certificates/confirmation-letter.pdf` | done |
| 3 | Course completion certificate | `certificates/completion.pdf` | done |
| 4 | Make the project repo public | `Savreet28/SkillTrend-AI` | **pending** — currently private, so the GitHub link 404s for visitors |

Only item 4 is outstanding, and it only affects the Project card's link.

---

## Viewing it locally

Open `index.html` by double-clicking it, or serve the folder:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

---

## Folder layout

```
TR103_DailyDiary_Savreet/
├── index.html              the website
├── style.css               purple theme, same palette as TR-102
├── gne-logo.png            college crest
├── worldwithweb-logo.png   company logo
├── build_pdfs.py           regenerates pdfs/ from docs/
├── docs/                   the diary content, as editable Markdown
│   ├── week1.md            Python Basics for Data Analysis
│   ├── week2.md            Data Cleaning, Statistics & EDA
│   ├── week3.md            SQL for Data Analysis
│   └── week4.md            Visualisation, Power BI & Mini Project
├── pdfs/                   generated — what the website links to
│   ├── week1.pdf
│   ├── week2.pdf
│   ├── week3.pdf
│   └── week4.pdf
└── certificates/
    ├── confirmation-letter.pdf   issued before training
    └── completion.pdf            issued 23 July 2026
```

---

## Editing the diary content

The Markdown files in `docs/` are the source. The PDFs are generated from them.

1. Edit `docs/week1.md` (or any week) in VS Code
2. Run the build:

```bash
python3 build_pdfs.py
```

3. Refresh the page

The script needs only Python 3 and Google Chrome — no `pip install`. It
converts each Markdown file to styled HTML and prints it to PDF using Chrome
in headless mode.

To change the *summary* text shown on a week's card on the homepage, edit
`index.html` directly — that text is separate from the PDF.

---

## Each week's content

| Week | Dates | Topics |
|---|---|---|
| 1 | 15 – 19 Jun | Python syntax, functions, NumPy, pandas, loading CSV/Excel |
| 2 | 22 – 26 Jun | Missing values, duplicates, outliers, descriptive statistics, correlation, t-tests, group-by, full EDA |
| 3 | 29 Jun – 3 Jul | SELECT/WHERE, aggregates, GROUP BY vs HAVING, joins, subqueries, CTEs, window functions, SQL from Python |
| 4 | 6 – 10 Jul | Matplotlib, Seaborn, chart choice, Power Query, star schema, DAX measures, dashboard, mini project |

The confirmation letter schedules the training as 15 June – 15 July 2026. The
four weekly logs cover the 20 working days from 15 June to 10 July.

Each week file contains five daily entries with the date, what was covered,
code examples, and a takeaway.

---

## Publishing to GitHub Pages

Same process as TR-102:

```bash
git init
git add .
git commit -m "TR-103 daily diary"
git branch -M main
git remote add origin https://github.com/Savreet28/TR103_DailyDiary_Savreet.git
git push -u origin main
```

Then in the repository: **Settings → Pages → Source: `main` / root**.

The site will be at `https://savreet28.github.io/TR103_DailyDiary_Savreet/`.

---

## Differences from the TR-102 site

Three small fixes, all optional to keep:

| Change | Reason |
|---|---|
| Poppins font is now actually loaded | `style.css` asks for Poppins but TR-102 never linked the font, so it fell back to a default sans-serif |
| `.pdf-link` and `.github-link` are styled | Both classes were used in TR-102's HTML but had no CSS rules, so they rendered as plain blue underlined links |
| Mobile breakpoint added | The header logos and title crowded each other below ~600px |
