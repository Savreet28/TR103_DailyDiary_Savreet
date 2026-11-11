# docs/ — the diary content

These four Markdown files are the **source** of the weekly diary. The PDFs the
website links to are generated from them.

| File | Week | Dates |
|---|---|---|
| `week1.md` | Python Basics for Data Analysis | 15 – 19 Jun 2026 |
| `week2.md` | Data Cleaning, Statistics & EDA | 22 – 26 Jun 2026 |
| `week3.md` | SQL for Data Analysis | 29 Jun – 3 Jul 2026 |
| `week4.md` | Visualisation, Power BI & Mini Project | 6 – 10 Jul 2026 |

## To change the content

1. Edit the Markdown file here
2. From the project root, run:

```bash
python3 build_pdfs.py
```

3. Refresh the website

Do **not** edit the files in `pdfs/` — they are overwritten every time the
build runs.

## Structure of each file

Each week follows the same shape, so they stay consistent:

```
# Week N — Title
   details block (organisation, trainee, period)
   Objective of the week

## Day N — Weekday, Date
   ### sub-topics, code examples, tables
   ### Takeaway

## Summary of Week N
   a table of the five days
   skills gained
```

## Supported Markdown

The build script handles headings, paragraphs, **bold**, *italic*, `inline
code`, fenced code blocks, bullet and numbered lists, pipe tables, and
horizontal rules. That covers everything the week files use.

Images and nested lists are not supported — if you need them, say so and the
converter can be extended.
