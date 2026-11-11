# Certificates

Both documents are in place and both cards on the website work.

| File | Document | Linked from |
|---|---|---|
| `confirmation-letter.pdf` | Training Confirmation Letter | Certificates card 1 |
| `completion.pdf` | Certificate of Completion | Certificates card 2 |

## confirmation-letter.pdf

Issued by World With Web before the training began, confirming enrolment in
the 4 Weeks Industrial Training Program in Data Analytics, scheduled
15 June 2026 to 15 July 2026.

## completion.pdf

Certificate of Completion, issued 23 July 2026.

- **Presented to:** Savreet Kaur
- **Course:** Data Analytics
- **Duration:** 4 Weeks
- **Period:** 15 June 2026 – 15 July 2026
- **Location:** Ludhiana, Feroze Gandhi Market
- **Sr. No.:** w03408

## Adding more certificates

Copy a whole `<a class="certificate-card-link">...</a>` block in the
certificates section of `index.html` and change the `href` and the title. The
grid wraps automatically, so extra cards lay out correctly with no CSS changes.

If you add a card for a document you do not have yet, give its inner div
`class="certificate-card is-pending"` — that greys it out and labels the slot
instead of leaving a broken link looking live.

## If a certificate is an image, not a PDF

Either convert it to PDF (on a Mac: open it in Preview → File → Export as
PDF), or keep the image and update the `href` in `index.html` to match the
filename you used.
