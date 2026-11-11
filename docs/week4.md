# Week 4 — Visualisation, Power BI & Mini Project

**Industrial Training TR-103 · Data Analytics**
**Organisation:** World With Web
**Trainee:** Savreet Kaur · URN 2302668
**Period:** 6 July 2026 – 10 July 2026

---

## Objective of the week

An analysis that nobody can read has not been delivered. This week covers
presenting results: charting in Python, the principles behind choosing a chart,
building an interactive dashboard in Power BI, and finally an end-to-end mini
project combining everything from the four weeks.

---

## Day 16 — Monday, 6 July 2026

### Matplotlib

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(monthly["month"], monthly["sales"], marker="o")
ax.set_title("Monthly Sales, 2026")
ax.set_xlabel("Month")
ax.set_ylabel("Sales (₹)")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()
```

Chart types covered and what each is for:

| Chart | Shows |
|---|---|
| Line | Change over time |
| Bar | Comparison across categories |
| Histogram | Distribution of one numeric column |
| Scatter | Relationship between two numeric columns |
| Box plot | Spread, median and outliers |
| Pie | Parts of a whole — used sparingly |

### Seaborn

Seaborn sits on top of Matplotlib with shorter syntax and better defaults for
statistical charts:

```python
import seaborn as sns

sns.boxplot(data=df, x="region", y="sales")
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="Purples")
sns.scatterplot(data=df, x="discount", y="profit", hue="category")
```

The correlation heatmap from Week 2 was redrawn here, and the negative
discount–profit relationship that was a number in a table became obvious at a
glance — which is the argument for visualisation in one example.

### Takeaway

Every chart needs a title, labelled axes and units. A chart without them forces
the reader to guess, and they will guess wrong.

---

## Day 17 — Tuesday, 7 July 2026

### Choosing the right chart

The rule given was to start from the question, not from the chart library:

| Question | Chart |
|---|---|
| How has this changed over time? | Line |
| Which category is largest? | Horizontal bar, sorted |
| How is this spread out? | Histogram or box plot |
| Are these two related? | Scatter |
| What share does each part hold? | Stacked bar (pie only for 2–3 parts) |

### Common mistakes

- **Truncated y-axis on a bar chart.** Starting at a non-zero value
  exaggerates small differences. Bars encode length, so the axis must start
  at zero. Line charts are different — they encode position, so a truncated
  axis is acceptable there.
- **Pie charts with many slices.** Humans compare angles poorly. Beyond about
  three categories a sorted bar chart is easier to read.
- **Dual axes.** Two different scales on one chart can be arranged to imply
  almost any relationship.
- **3D effects.** They distort the very lengths and areas the chart exists to
  convey.
- **Rainbow colour scales.** They imply category boundaries that are not in
  the data. A single-hue scale is better for continuous values.

### Dashboard design principles

1. One dashboard answers one question
2. Most important number top-left, where the eye lands first
3. Group related charts together
4. Consistent colours — one colour means one thing throughout
5. Leave white space; a crowded dashboard is not more informative
6. Label units and state the time period covered

### Takeaway

Chart design is mostly about *not* misleading. The default settings of most
tools are optimised to look impressive, not to be read accurately.

---

## Day 18 — Wednesday, 8 July 2026

### Power BI Desktop

The interface was introduced: the Report, Data and Model views, the Fields
pane, the Visualizations pane, and Filters.

### Getting data

Data was imported from three sources — Excel, CSV and a SQL database — to show
that the connector changes but the rest of the workflow does not.

### Power Query Editor

Transformations applied before the data reaches the model:

- Promote the first row to headers
- Set the correct data type on every column
- Remove unnecessary columns
- Replace values and handle nulls
- Split and merge columns
- Unpivot columns — turning a wide monthly layout into a tidy long one

Every step is recorded in **Applied Steps** on the right, so the sequence is
visible, re-runnable on refreshed data, and removable if wrong. This is an
advantage over cleaning in Excel by hand, where the steps leave no trace.

### The data model

Separate tables were related rather than merged into one wide table:

- `Sales` (fact table) → `Products` (dimension) via `product_id`
- `Sales` (fact) → `Customers` (dimension) via `customer_id`
- `Sales` (fact) → `Calendar` (dimension) via `date`

This is the **star schema**, and it is the same relational thinking as the SQL
joins of Week 3 — the difference is that the relationship is declared once in
the model instead of written into every query.

### Takeaway

Time spent in Power Query and the model view is repaid in every visual
afterwards. Fixing the model later means rebuilding the visuals.

---

## Day 19 — Thursday, 9 July 2026

### DAX basics

DAX (Data Analysis Expressions) is the formula language of Power BI.

**Calculated column** — computed per row, stored in the table:

```dax
Line Total = Sales[quantity] * Sales[unit_price]
```

**Measure** — computed at query time, respecting the current filters:

```dax
Total Revenue = SUM(Sales[Line Total])

Total Orders = DISTINCTCOUNT(Sales[order_id])

Average Order Value = DIVIDE([Total Revenue], [Total Orders])
```

`DIVIDE` was recommended over the `/` operator because it handles division by
zero without producing an error across the whole visual.

The distinction that mattered most: a **column** is fixed when the data
refreshes; a **measure** recalculates for whatever slice the user has selected.
Totals, averages and counts should almost always be measures.

### Time intelligence

```dax
Revenue LY =
CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Calendar'[Date]))

YoY Growth % =
DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY])
```

These require a proper date table marked as the date table in the model.

### Building the dashboard

A sales dashboard was assembled:

- **KPI cards** — total revenue, total orders, average order value
- **Line chart** — revenue by month
- **Bar chart** — revenue by category, sorted descending
- **Map** — revenue by city
- **Table** — top 10 customers
- **Slicers** — date range, region, category

Interactions were configured so that selecting a bar filters every other
visual, and the KPI cards update accordingly.

### Takeaway

The slicers are what make a dashboard worth building. A static report answers
the questions its author thought of; an interactive one lets the reader ask
their own.

---

## Day 20 — Friday, 10 July 2026

### Mini project — end-to-end analysis

The final day combined all four weeks into a single piece of work.

**Dataset:** a retail sales dataset with roughly 10,000 order rows across
customers, products, regions and dates.

**Process:**

| Step | Tool | Week |
|---|---|---|
| 1. Load and inspect | pandas | 1 |
| 2. Clean — types, nulls, duplicates | pandas | 2 |
| 3. Explore — distributions, correlation | pandas, Seaborn | 2 |
| 4. Aggregate — revenue by region, category, month | SQL | 3 |
| 5. Visualise — dashboard with slicers | Power BI | 4 |
| 6. Present — findings and recommendations | — | 4 |

**Findings presented:**

1. Revenue is concentrated — the top 20 per cent of customers account for a
   little over half of total revenue
2. Discounts above roughly 30 per cent turn profit negative, consistent with
   the correlation found in Week 2
3. One region underperforms on revenue despite a comparable order count,
   because its average order value is lower
4. Sales peak at year end, with the pattern repeating across the period

**Recommendations:** cap discounts at the point where profit turns negative,
target the low average-order-value region with bundles rather than discounts,
and plan stock for the year-end peak.

### Training wrap-up

The project was presented to the trainer, followed by a review of the four
weeks, questions, and feedback on the dashboard.

### Takeaway

The analysis was the straightforward part. Deciding what mattered enough to
show, and saying it in sentences a non-technical reader could act on, took
longer than producing the numbers.

---

## Summary of Week 4

| Day | Date | Topic |
|---|---|---|
| 16 | Mon 6 Jul | Matplotlib and Seaborn |
| 17 | Tue 7 Jul | Choosing charts; dashboard design |
| 18 | Wed 8 Jul | Power BI, Power Query, data model |
| 19 | Thu 9 Jul | DAX measures, time intelligence, dashboard |
| 20 | Fri 10 Jul | Mini project and final presentation |

**Skills gained:** charting with Matplotlib and Seaborn · choosing a chart that
does not mislead · Power Query transformations · star-schema data modelling ·
DAX measures and time intelligence · building an interactive dashboard ·
presenting findings as recommendations.

---

## Overall training outcome

| Week | Focus | Core skill |
|---|---|---|
| 1 | Python Basics | Load and inspect any dataset |
| 2 | Cleaning, Statistics, EDA | Fix the data and describe it honestly |
| 3 | SQL | Query a real database analytically |
| 4 | Visualisation & Power BI | Communicate the result |

Across the four weeks the training covered the full path a data analyst
follows: raw data in, cleaned and understood in the middle, a decision
supported at the end. The mini project exercised every stage of it.
