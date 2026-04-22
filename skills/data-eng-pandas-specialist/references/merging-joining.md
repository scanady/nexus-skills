# Merging & Joining

Combine DataFrames: SQL-style merge, index-based join, concat. pandas 2.0+.

---

## Join Type Decision Table

| Goal | `how=` | Result |
|------|--------|--------|
| Only matching rows from both | `inner` (default) | Intersection |
| All left + matching right | `left` | Left preserved, right NaN where no match |
| All right + matching left | `right` | Right preserved, left NaN where no match |
| All rows from both | `outer` | Union, NaN where no match on either side |
| Cartesian product | `cross` | All combinations |

---

## `pd.merge()` — SQL-Style Join

### Same Key Name

```python
import pandas as pd
import numpy as np

employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'dept_id': [101, 102, 101, 103, 102],
})
departments = pd.DataFrame({
    'dept_id': [101, 102, 104],
    'dept_name': ['Engineering', 'Sales', 'Marketing'],
})

inner = pd.merge(employees, departments, on='dept_id')                # 4 rows
left  = pd.merge(employees, departments, on='dept_id', how='left')   # 5 rows
outer = pd.merge(employees, departments, on='dept_id', how='outer')  # 6 rows
```

### Different Key Names

```python
result = pd.merge(employees, departments, left_on='dept_id', right_on='id')
result = result.drop(columns=['id'])  # Drop duplicate key column
```

### Multi-Column Key

```python
result = pd.merge(sales, targets, on=['region', 'product'], how='left')
```

### Join on Index

```python
emp_idx = employees.set_index('emp_id')
sal_idx = salaries.set_index('emp_id')

result = pd.merge(emp_idx, sal_idx, left_index=True, right_index=True)

# Mix: column on left, index on right
result = pd.merge(employees, sal_idx, left_on='emp_id', right_index=True)
```

---

## Duplicate Column Handling

```python
# Default suffixes: _x, _y
result = pd.merge(df1, df2, on='id')

# Custom suffixes
result = pd.merge(df1, df2, on='id', suffixes=('_jan', '_feb'))
```

---

## Validate Cardinality

Raises `MergeError` if expectation violated — use to catch bad data upstream.

```python
# One-to-one: key unique in both
pd.merge(df1, df2, on='id', validate='1:1')

# One-to-many: key unique in left
pd.merge(employees, orders, on='emp_id', validate='1:m')

# Many-to-one: key unique in right
pd.merge(orders, employees, on='emp_id', validate='m:1')
```

---

## Indicator Column — Debug Merge Coverage

```python
result = pd.merge(
    employees, departments,
    on='dept_id',
    how='outer',
    indicator=True,         # Adds _merge column
)
# _merge values: 'left_only', 'right_only', 'both'

# Filter by source
unmatched_employees = result[result['_merge'] == 'left_only']
```

---

## `.join()` — Index-Based (Shorthand)

```python
# Simple index-to-index join
result = employees.join(salaries)           # Default: left join on index
result = employees.join(salaries, how='outer')

# Left column to right index
result = employees.join(departments, on='dept_id')

# Join multiple DataFrames at once
result = df1.join([df2, df3])
```

---

## `pd.concat()` — Stack DataFrames

### Vertical (row-wise, axis=0)

```python
# Stack rows
result = pd.concat([df1, df2])

# Reset integer index
result = pd.concat([df1, df2], ignore_index=True)

# Track source with MultiIndex
result = pd.concat([df1, df2], keys=['batch_1', 'batch_2'])

# Mismatched columns → NaN fills gaps (default join='outer')
result = pd.concat([df1, df2], join='outer')   # All columns
result = pd.concat([df1, df2], join='inner')   # Common columns only
```

### Horizontal (column-wise, axis=1)

```python
result = pd.concat([names, ages, salaries], axis=1)
```

### Concat vs Merge

| Use | When |
|-----|------|
| `pd.merge()` | Joining on a key — SQL-style |
| `.join()` | Joining on index |
| `pd.concat()` | Stacking rows or columns from same-schema DataFrames |
