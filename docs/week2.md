# Week 2 — Data Cleaning, Statistics & Exploratory Data Analysis

**Industrial Training TR-103 · Data Analytics**
**Organisation:** World With Web
**Trainee:** Savreet Kaur · URN 2302668
**Period:** 22 June 2026 – 26 June 2026

---

## Objective of the week

Week 1 ended with loading a dataset and seeing its problems. This week is
about fixing those problems and then describing what remains: missing values,
duplicates and outliers first, then descriptive statistics, relationships
between variables, and a complete exploratory analysis.

---

## Day 6 — Monday, 22 June 2026

### Missing values

Three questions must be answered before anything is changed: how much is
missing, where, and why.

```python
df.isnull().sum()                      # count per column
df.isnull().mean().mul(100).round(1)   # percentage per column
```

Handling strategies and when each applies:

| Strategy | Code | Appropriate when |
|---|---|---|
| Drop rows | `df.dropna()` | Few rows affected, data is plentiful |
| Drop column | `df.drop(columns=[...])` | Column is mostly empty and not essential |
| Fill constant | `df.fillna(0)` | Missing genuinely means zero |
| Fill mean | `df["x"].fillna(df["x"].mean())` | Roughly symmetric numeric data |
| Fill median | `df["x"].fillna(df["x"].median())` | Skewed data, or outliers present |
| Forward fill | `df.ffill()` | Time series where the last value persists |

The point stressed repeatedly was that **filling is an assumption**. Replacing
missing salaries with the mean does not recover the real values; it makes the
column usable while reducing its apparent variance. Any such choice should be
recorded.

### Duplicates

```python
df.duplicated().sum()
df = df.drop_duplicates()
df = df.drop_duplicates(subset=["order_id"], keep="first")
```

The distinction between a fully duplicated row and a repeated key was
covered — the second often indicates a genuine data-entry problem rather than
a harmless repeat.

### Data types

Numeric columns read as text are the most common silent defect, usually caused
by stray symbols:

```python
df["amount"] = (df["amount"]
                .str.replace(",", "", regex=False)
                .str.replace("₹", "", regex=False)
                .astype(float))

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
```

`errors="coerce"` turns unparseable dates into `NaT` rather than raising, so
the bad rows can be counted and inspected instead of stopping the script.

### Takeaway

Cleaning is not a preliminary step to the analysis — the decisions made here
determine what the analysis is able to say.

---

## Day 7 — Tuesday, 23 June 2026

### Measures of central tendency

| Measure | Meaning | Sensitive to outliers |
|---|---|---|
| Mean | Arithmetic average | Yes |
| Median | Middle value when sorted | No |
| Mode | Most frequent value | No |

The worked example made the difference concrete: in a salary column with a few
very high values, the mean sat above the median, and the mean described almost
nobody in the dataset. The rule given was to report the median for skewed data
and to state which was used.

### Measures of spread

- **Range** — maximum minus minimum; entirely determined by two points
- **Variance** — mean squared deviation from the mean
- **Standard deviation** — square root of variance, in the original units
- **IQR** — Q3 minus Q1, the middle 50 per cent of the data

```python
df["salary"].describe()

q1, q3 = df["salary"].quantile([0.25, 0.75])
iqr = q3 - q1
```

### Takeaway

Standard deviation is readable because it is in the same unit as the data;
variance is not. Both describe the same thing.

---

## Day 8 — Wednesday, 24 June 2026

### Distributions

Histograms and box plots were used to see the shape of a column rather than
only its summary numbers.

- **Normal** — symmetric, mean ≈ median
- **Right-skewed** — a long tail of high values; mean > median. Income,
  prices and web traffic are typically this shape.
- **Left-skewed** — a long tail of low values; mean < median

### Outlier detection

**IQR method** — anything outside 1.5 × IQR beyond the quartiles:

```python
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
outliers = df[(df["salary"] < lower) | (df["salary"] > upper)]
```

**Z-score method** — anything more than 3 standard deviations from the mean.
Noted as unreliable on skewed data, because the mean and standard deviation
used to compute it are themselves distorted by the outliers.

### What to do with an outlier

Four options were discussed, in order of preference: investigate it, keep it,
cap it (winsorise), or remove it. Removing should be the last resort and must
be recorded — a genuine extreme value is data, and deleting it to make a chart
look tidier is falsifying the result.

### Takeaway

An outlier is not automatically an error. A data-entry mistake and a genuinely
exceptional customer look identical in the numbers; only context separates them.

---

## Day 9 — Thursday, 25 June 2026

### Correlation

```python
df[["sales", "profit", "discount"]].corr()
```

Pearson's correlation coefficient runs from −1 to +1 and measures the strength
of a **linear** relationship.

| Range | Interpretation |
|---|---|
| 0.7 to 1.0 | Strong positive |
| 0.3 to 0.7 | Moderate positive |
| −0.3 to 0.3 | Weak or none |
| −1.0 to −0.7 | Strong negative |

Two cautions were emphasised. A coefficient near zero rules out a *linear*
relationship, not any relationship — a clear curve can score near zero. And
correlation does not imply causation; the standard counter-example of ice-cream
sales and drowning incidents, both driven by temperature, was used.

### Introduction to hypothesis testing

- **Null hypothesis (H₀)** — there is no effect or no difference
- **Alternative hypothesis (H₁)** — there is one
- **p-value** — the probability of seeing a result at least this extreme if H₀
  were true
- **Significance level (α)** — conventionally 0.05

A two-sample t-test was run comparing the mean sales of two regions:

```python
from scipy import stats

north = df[df["region"] == "North"]["sales"]
south = df[df["region"] == "South"]["sales"]
t_stat, p_value = stats.ttest_ind(north, south, equal_var=False)
```

The interpretation was stated carefully: a p-value below 0.05 means the data
would be unlikely under the null hypothesis. It does not give the probability
that the null hypothesis is true, and it says nothing about whether the
difference is large enough to matter in practice.

### Takeaway

Statistical significance and practical importance are different questions. With
a large enough sample, a trivial difference becomes significant.

---

## Day 10 — Friday, 26 June 2026

### Grouping and aggregation

```python
df.groupby("region")["sales"].sum()

df.groupby(["region", "category"]).agg(
    total_sales=("sales", "sum"),
    avg_profit=("profit", "mean"),
    orders=("order_id", "count"),
).reset_index()
```

The split–apply–combine idea was explained as the direct counterpart of SQL's
`GROUP BY`, which Week 3 covers.

### Pivot tables

```python
pd.pivot_table(df, index="region", columns="category",
               values="sales", aggfunc="sum", fill_value=0)
```

### Full EDA on a sample dataset

The week closed with an end-to-end exploratory analysis of a retail sales
dataset, following a fixed sequence:

1. Load and inspect — shape, types, nulls
2. Clean — fix types, handle missing values, remove duplicates
3. Univariate analysis — distribution of each important column
4. Bivariate analysis — relationships between pairs of columns
5. Grouped summaries — by region, category and month
6. Write down the findings in plain sentences

### Findings recorded

- Sales are right-skewed: most orders are small, a few are very large
- One region accounts for a disproportionate share of total revenue
- Discount and profit are negatively correlated, with profit turning negative
  above roughly a 30 per cent discount
- Monthly sales show a clear year-end peak

### Takeaway

Exploratory analysis is for forming questions, not confirming conclusions. Each
finding above is a hypothesis to test, not a result to report as settled.

---

## Summary of Week 2

| Day | Date | Topic |
|---|---|---|
| 6 | Mon 22 Jun | Missing values, duplicates, data types |
| 7 | Tue 23 Jun | Central tendency and spread |
| 8 | Wed 24 Jun | Distributions, skewness, outliers |
| 9 | Thu 25 Jun | Correlation and hypothesis testing |
| 10 | Fri 26 Jun | Group-by, pivot tables, complete EDA |

**Skills gained:** cleaning a messy dataset and documenting the choices ·
describing data with the right summary statistic · detecting outliers ·
reading a correlation matrix · running and interpreting a t-test · performing
a structured exploratory analysis.

**Next week:** the same questions, answered against a database using SQL.
