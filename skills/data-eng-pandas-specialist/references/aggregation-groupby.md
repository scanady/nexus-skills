# Aggregation & GroupBy

GroupBy, named aggregation, transform, apply, pivot, melt, crosstab. pandas 2.0+.

---

## GroupBy Basics

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'dept': ['Eng', 'Eng', 'Sales', 'Sales', 'Eng', 'HR'],
    'team': ['Backend', 'Frontend', 'East', 'West', 'Backend', 'Recruit'],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
    'salary': [80000, 75000, 65000, 70000, 85000, 60000],
    'years': [5, 3, 7, 4, 6, 2],
})

# Single group, single stat
df.groupby('dept')['salary'].mean()

# Single group, multiple stats
df.groupby('dept')['salary'].agg(['mean', 'min', 'max', 'count'])

# Multi-column group
df.groupby(['dept', 'team'])['salary'].mean()

# Return DataFrame (not Series)
df.groupby('dept')['salary'].mean().reset_index()
```

---

## Named Aggregation (Preferred, pandas 2.0+)

Cleaner than dict syntax — output column names explicit.

```python
result = df.groupby('dept').agg(
    avg_salary=('salary', 'mean'),
    max_salary=('salary', 'max'),
    total_years=('years', 'sum'),
    headcount=('name', 'count'),
)

# Custom function in named agg
def salary_range(x):
    return x.max() - x.min()

result = df.groupby('dept').agg(
    sal_range=('salary', salary_range),
    sal_p75=('salary', lambda x: x.quantile(0.75)),
    sal_cv=('salary', lambda x: x.std() / x.mean()),
)
```

---

## Transform — Same Shape Back to Original

Use when adding aggregated values as new columns in the original DataFrame.

```python
# Group mean as new column
df['dept_avg'] = df.groupby('dept')['salary'].transform('mean')

# Z-score within group
df['sal_z'] = df.groupby('dept')['salary'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# Rank within group (highest salary = rank 1)
df['sal_rank'] = df.groupby('dept')['salary'].transform('rank', ascending=False)

# % of group total
df['sal_pct'] = df.groupby('dept')['salary'].transform(
    lambda x: x / x.sum() * 100
)

# Fill nulls with group mean
df['salary'] = df.groupby('dept')['salary'].transform(
    lambda x: x.fillna(x.mean())
)
```

---

## Apply — Flexible Group Logic

Use when transform can't express the logic. Slower than vectorized — profile before scaling.

```python
# Return top N earners per group
def top_n(group, n=2):
    return group.nlargest(n, 'salary')

top_earners = df.groupby('dept', group_keys=False).apply(top_n, n=2).reset_index(drop=True)

# Return summary Series per group
def group_summary(g):
    return pd.Series({
        'headcount': len(g),
        'avg_salary': g['salary'].mean(),
        'top_earner': g.loc[g['salary'].idxmax(), 'name'],
        'avg_tenure': g['years'].mean(),
    })

summary = df.groupby('dept').apply(group_summary)
```

---

## Filter — Keep / Drop Entire Groups

```python
# Groups with avg salary > 70k
df.groupby('dept').filter(lambda x: x['salary'].mean() > 70000)

# Groups with >= 2 members
df.groupby('dept').filter(lambda x: len(x) >= 2)

# Combined
df.groupby('dept').filter(
    lambda x: len(x) >= 2 and x['salary'].mean() > 65000
)
```

---

## Pivot Tables

```python
sales = pd.DataFrame({
    'product': ['A', 'B', 'A', 'B', 'A', 'B'],
    'region': ['East', 'East', 'West', 'West', 'East', 'West'],
    'sales': [100, 150, 120, 180, 90, 200],
    'qty': [10, 15, 12, 18, 9, 20],
})

# Basic
pivot = sales.pivot_table(values='sales', index='product', columns='region', aggfunc='sum')

# Multiple values + fill missing
pivot = sales.pivot_table(
    values=['sales', 'qty'],
    index='product',
    columns='region',
    aggfunc='sum',
    fill_value=0,
)

# With row/column totals
pivot = sales.pivot_table(
    values='sales',
    index='product',
    columns='region',
    aggfunc='sum',
    margins=True,
    margins_name='Total',
)

# observed=True required for categorical columns (pandas 2.0+)
pivot = sales.pivot_table(
    values='sales',
    index='product',
    columns='region',
    aggfunc='sum',
    observed=True,
)
```

### Melt — Wide to Long

```python
wide = pd.DataFrame({
    'product': ['A', 'B'],
    'Q1': [100, 150],
    'Q2': [120, 180],
    'Q3': [90, 200],
})

long = pd.melt(
    wide,
    id_vars=['product'],
    value_vars=['Q1', 'Q2', 'Q3'],
    var_name='quarter',
    value_name='sales',
)
```

---

## Crosstab

```python
df = pd.DataFrame({
    'gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'M'],
    'dept': ['Eng', 'Eng', 'Sales', 'Sales', 'Eng', 'HR', 'HR', 'Eng'],
})

# Counts
pd.crosstab(df['gender'], df['dept'])

# Normalized — row, column, or total
pd.crosstab(df['gender'], df['dept'], normalize='index')    # Row %
pd.crosstab(df['gender'], df['dept'], normalize='columns')  # Column %
pd.crosstab(df['gender'], df['dept'], normalize='all')      # Grand total %

# With margins
pd.crosstab(df['gender'], df['dept'], margins=True)

# Multi-level index
pd.crosstab([df['gender'], df['dept']], df['dept'])
```
