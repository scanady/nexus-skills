# Data Cleaning

Missing values, duplicates, type conversion, string normalization. pandas 2.0+.

---

## Null Handling Strategy

Decide before acting:

| Missing % | Typical action |
|-----------|----------------|
| < 5% | Fill with stat (mean/median/mode) or drop rows |
| 5–30% | Fill with group stat or model-imputed value |
| > 30% | Drop column or flag as feature |
| All nulls | Drop column |

---

## Detect Nulls

```python
import pandas as pd
import numpy as np

# Per column
df.isna().sum()
(df.isna().sum() / len(df) * 100).round(2)   # Percent missing

# Any null
df.isna().any().any()

# Rows with any null
df[df.isna().any(axis=1)]

# Summary profile
pd.DataFrame({
    'missing': df.isna().sum(),
    'pct': (df.isna().sum() / len(df) * 100).round(2),
    'dtype': df.dtypes,
}).query('missing > 0')
```

---

## Fill Nulls

```python
# Constant
df['age'] = df['age'].fillna(0)

# Column statistics
df['age'] = df['age'].fillna(df['age'].mean())
df['salary'] = df['salary'].fillna(df['salary'].median())
df['dept'] = df['dept'].fillna(df['dept'].mode()[0])

# Forward / backward fill (time series or ordered data)
df['price'] = df['price'].ffill()
df['price'] = df['price'].bfill()

# Linear interpolation
df['value'] = df['value'].interpolate(method='linear')

# Multiple columns at once
df = df.fillna({'age': 0, 'salary': df['salary'].median(), 'name': 'Unknown'})

# Fill with group stat (preserves group context)
df['salary'] = df.groupby('dept')['salary'].transform(
    lambda x: x.fillna(x.mean())
)
```

---

## Drop Nulls

```python
df.dropna()                                  # Any null in any column
df.dropna(subset=['name', 'age'])            # Null in specific columns only
df.dropna(how='all')                         # Only drop if all values null
df.dropna(thresh=3)                          # Keep if >= 3 non-null values
df.dropna(axis=1)                            # Drop columns with nulls
df.dropna(axis=1, thresh=int(len(df) * 0.5))  # Drop columns > 50% null
```

---

## Empty Strings vs NaN

Empty strings are NOT null — detect and replace explicitly.

```python
# Single replacement
df['dept'] = df['dept'].replace('', np.nan)

# Whitespace-only strings
df['dept'] = df['dept'].replace(r'^\s*$', np.nan, regex=True)

# Multiple sentinel values
df = df.replace(['', 'N/A', 'null', 'None', '-'], np.nan)

# At read time (most efficient)
df = pd.read_csv('file.csv', na_values=['', 'N/A', 'null', 'None', '-'])
```

---

## Duplicates

### Detect

```python
df.duplicated().sum()                         # Total duplicate rows
df.duplicated(subset=['id']).sum()            # Duplicate on key column
df[df.duplicated(keep=False)]                 # All instances of duplicates
df[df.duplicated(keep='first')]               # All except first occurrence
```

### Remove

```python
df.drop_duplicates()                          # Keep first (default)
df.drop_duplicates(keep='last')
df.drop_duplicates(keep=False)                # Drop all copies
df.drop_duplicates(subset=['id', 'email'], keep='last')
```

### Aggregate Duplicates Instead of Dropping

```python
# Keep row with max value per key
df.loc[df.groupby('id')['score'].idxmax()]

# Combine duplicate values
df.groupby('id').agg({
    'name': 'first',
    'email': lambda x: ', '.join(x.unique())
}).reset_index()
```

---

## Type Conversion

### Numeric

```python
df['age'] = df['age'].astype(int)
df['price'] = df['price'].astype(float)

# Safe — coerce invalid to NaN
df['age'] = pd.to_numeric(df['age'], errors='coerce')

# Multiple columns
df = df.astype({'age': 'int64', 'price': 'float64'})
```

### Datetime

```python
df['date'] = pd.to_datetime(df['date_str'], errors='coerce')

# Specify format for faster parse
df['date'] = pd.to_datetime(df['date_str'], format='%Y-%m-%d', errors='coerce')

# Unix timestamp
df['dt'] = pd.to_datetime(df['ts'], unit='s')

# Mixed formats (pandas 2.0+)
df['date'] = pd.to_datetime(df['date_str'], format='mixed')

# Extract components
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['dow'] = df['date'].dt.day_name()
```

### Categorical

```python
# Low-cardinality string → category saves memory
df['dept'] = df['dept'].astype('category')

# Ordered categorical
df['size'] = pd.Categorical(
    df['size'],
    categories=['S', 'M', 'L', 'XL'],
    ordered=True
)
```

### Nullable Types (pandas 2.0+)

```python
# Standard int64 can't hold NaN — use nullable types
df = df.astype({
    'count': 'Int64',      # Nullable integer
    'price': 'Float64',    # Nullable float
    'active': 'boolean',   # Nullable bool
    'name': 'string',      # Nullable string
})

# Arrow-backed (best memory + interop)
df['name'] = df['name'].astype('string[pyarrow]')
```

---

## String Cleaning

```python
df['name'] = df['name'].str.strip()               # Remove surrounding whitespace
df['name'] = df['name'].str.lower()               # Normalize case
df['name'] = df['name'].str.title()               # Title Case
df['name'] = df['name'].str.replace(r'\s+', ' ', regex=True)  # Collapse spaces
df['phone'] = df['phone'].str.replace(r'[^0-9]', '', regex=True)  # Digits only

# Extract substring
df['domain'] = df['email'].str.split('@').str[1]

# Validate format
valid = df['email'].str.match(r'^[\w.+-]+@[\w-]+\.[a-z]{2,}$')
df = df[valid]
```
