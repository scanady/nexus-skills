# DataFrame Operations

Core indexing, selection, filtering, sorting, and column manipulation. pandas 2.0+.

---

## Selection Quick-Reference

| Goal | Use | Why |
|------|-----|-----|
| Filter by condition | `.loc[mask, cols]` | Label-based, readable |
| Named columns, any rows | `.loc[:, 'col']` | Explicit column name |
| First/last N rows | `.iloc[:5]` / `.iloc[-5:]` | Position-based |
| Unknown column order | `.iloc[:, 0]` | Integer position |
| Specific row positions | `.iloc[[0, 5, 10]]` | Position list |

---

## `.loc[]` — Label-Based

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'age': [25, 30, 35, 28],
    'salary': [50000, 60000, 70000, 55000],
    'dept': ['Eng', 'Sales', 'Eng', 'Marketing']
}, index=['a', 'b', 'c', 'd'])

# Single value
df.loc['a', 'name']

# Single row → Series
df.loc['a']

# Multiple rows
df.loc[['a', 'c']]

# Row + column slice (inclusive both ends)
df.loc['a':'c', 'name':'salary']

# Boolean filter
df.loc[df['age'] >= 30]

# Boolean filter + column selection
df.loc[df['age'] >= 30, 'name']

# Multi-condition (always use parentheses)
df.loc[(df['dept'] == 'Eng') & (df['age'] >= 30), ['name', 'salary']]
```

---

## `.iloc[]` — Position-Based

```python
df.iloc[0, 0]          # Single value at [row 0, col 0]
df.iloc[0]             # First row → Series
df.iloc[:3]            # First three rows
df.iloc[[0, 2], [0, 2]]  # Rows 0,2 and columns 0,2
df.iloc[1:3, 0:2]      # Rows 1–2, columns 0–1 (exclusive end)
```

---

## Filtering Patterns

### Boolean Masks

```python
# Single condition
filtered = df[df['age'] > 25]

# AND / OR (parentheses required)
filtered = df[(df['age'] > 25) & (df['salary'] < 65000)]
filtered = df[(df['dept'] == 'Eng') | (df['dept'] == 'Sales')]

# NOT
filtered = df[~(df['dept'] == 'Marketing')]
```

### `.query()` — Readable Multi-Condition

```python
result = df.query('age > 25 and salary < 65000')

# External variable
min_age = 25
result = df.query('age > @min_age')

# In-list filter
depts = ['Eng', 'Sales']
result = df.query('dept in @depts')
```

### `.isin()` — Multi-Value Match

```python
filtered = df[df['dept'].isin(['Eng', 'Sales'])]
filtered = df[~df['dept'].isin(['Eng', 'Sales'])]  # Negation
```

### String Filters via `.str`

```python
df[df['name'].str.startswith('A')]
df[df['name'].str.contains('alice', case=False)]
df[df['name'].str.match(r'^[A-Z][a-z]+$')]
# Handle NaN in string columns
df[df['name'].str.contains('Alice', na=False)]
```

---

## Sorting

```python
# Single column
df.sort_values('age')
df.sort_values('age', ascending=False)

# Multiple columns
df.sort_values(['dept', 'salary'], ascending=[True, False])

# NaN placement
df.sort_values('salary', na_position='last')   # default
df.sort_values('salary', na_position='first')

# Custom categorical order
order = ['Marketing', 'Sales', 'Eng']
df['dept'] = pd.Categorical(df['dept'], categories=order, ordered=True)
df.sort_values('dept')

# Sort then reset index (chained)
df = df.sort_values('age').reset_index(drop=True)
```

---

## Column Operations

### Add / Modify

```python
# New column (vectorized)
df['bonus'] = df['salary'] * 0.1

# Conditional column
df['level'] = np.where(df['age'] >= 30, 'Senior', 'Junior')

# Multiple conditions
df['band'] = np.select(
    [df['age'] < 25, df['age'] < 35, df['age'] >= 35],
    ['Junior', 'Mid', 'Senior'],
    default='Unknown'
)

# Method chaining with .assign() — returns new DataFrame
df_new = df.assign(
    bonus=lambda x: x['salary'] * 0.1,
    total_comp=lambda x: x['salary'] * 1.1
)
```

### Rename

```python
df = df.rename(columns={'name': 'full_name', 'dept': 'department'})
df.columns = df.columns.str.lower().str.replace(' ', '_')  # Normalize all
```

### Drop

```python
df = df.drop(columns=['bonus'])
df = df.drop(columns=['bonus', 'band'])

# Drop by prefix
df = df.drop(columns=[c for c in df.columns if c.startswith('temp_')])
```

### Reorder

```python
df = df[['name', 'dept', 'age', 'salary']]  # Explicit order

# Move one column to front
cols = ['salary'] + [c for c in df.columns if c != 'salary']
df = df[cols]
```
