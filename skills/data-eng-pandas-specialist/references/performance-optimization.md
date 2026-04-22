# Performance Optimization

Memory profiling, dtype reduction, vectorization, chunked I/O. pandas 2.0+.

---

## Memory Quick-Wins

| Optimization | Typical savings |
|---|---|
| `object` → `category` (low cardinality) | 50–95% per column |
| `float64` → `float32` | 50% per column |
| `int64` → `int32` / `int16` | 25–50% per column |
| `string[pyarrow]` over `object` | 30–50% + faster ops |
| Nullable types (`Int32`, `Float32`) | Enables downcast with NA support |

---

## Memory Profile

Check usage before optimizing — measure, then act.

```python
import pandas as pd
import numpy as np

def memory_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Column-level memory usage with optimization hints."""
    usage = df.memory_usage(deep=True)
    profile = pd.DataFrame({
        'dtype': df.dtypes,
        'non_null': df.count(),
        'null_count': df.isna().sum(),
        'unique': df.nunique(),
        'mem_mb': (usage / 1e6).round(3),
    })

    hints = []
    for col in df.columns:
        dtype = df[col].dtype
        n_unique = df[col].nunique()
        if dtype == 'object':
            hint = f'→ category ({n_unique} unique)' if n_unique / len(df) < 0.5 else '→ string[pyarrow]'
        elif dtype == 'int64':
            if df[col].between(-2**15, 2**15 - 1).all():
                hint = '→ Int16'
            elif df[col].between(-2**31, 2**31 - 1).all():
                hint = '→ Int32'
            else:
                hint = 'OK'
        elif dtype == 'float64':
            hint = '→ Float32 (if precision ok)'
        else:
            hint = 'OK'
        hints.append(hint)

    profile['hint'] = hints
    return profile

print(memory_profile(df))
print(f"Total: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
```

---

## Dtype Optimization

### Downcast Numerics

```python
# Auto-downcast integers
df['count'] = pd.to_numeric(df['count'], downcast='integer')

# Auto-downcast floats
df['value'] = pd.to_numeric(df['value'], downcast='float')

# Batch downcast all numerics
def downcast_numerics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.select_dtypes('int').columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    for col in df.select_dtypes('float').columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    return df
```

### Categorical Columns

```python
# Manual
df['dept'] = df['dept'].astype('category')

# Auto-convert low-cardinality object columns
def auto_categorize(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    df = df.copy()
    for col in df.select_dtypes('object').columns:
        if df[col].nunique() / len(df) < threshold:
            df[col] = df[col].astype('category')
    return df
```

### Nullable + Arrow-Backed Types

```python
# Nullable types — support NaN without float promotion
df = df.astype({
    'id': 'Int32',
    'count': 'Int16',
    'price': 'Float32',
    'active': 'boolean',
    'name': 'string',       # Nullable string
})

# Arrow-backed — better memory + faster ops (pandas 2.0+)
df['name'] = df['name'].astype('string[pyarrow]')
df['category'] = df['category'].astype('category')
```

---

## Vectorization — Never Loop

### Replace `.iterrows()` with Vectorized Ops

```python
# BAD — row loop
result = []
for _, row in df.iterrows():
    result.append(row['value'] * 2 if row['value'] > 0 else 0)
df['result'] = result

# GOOD — vectorized
df['result'] = np.where(df['value'] > 0, df['value'] * 2, 0)
```

### Multi-Condition: `np.select`

```python
# BAD — apply with if/else
df['band'] = df.apply(lambda r: 'high' if r['v'] > 1 else ('low' if r['v'] < -1 else 'mid'), axis=1)

# GOOD — np.select
df['band'] = np.select(
    [df['v'] < -1, df['v'] < 1],
    ['low', 'mid'],
    default='high',
)
```

### String Ops — Use `.str` Accessor

```python
# BAD
df['upper'] = df['name'].apply(lambda x: x.upper())

# GOOD
df['upper'] = df['name'].str.upper()
df['clean'] = df['name'].str.strip().str.lower().str.replace(r'\s+', '_', regex=True)
```

### Direct Column Arithmetic — Skip `.apply()`

```python
# BAD
df['total'] = df.apply(lambda r: r['a'] + r['b'] + r['c'], axis=1)

# GOOD
df['total'] = df['a'] + df['b'] + df['c']
```

### When `.apply()` IS Acceptable

- Complex multi-column conditional logic with no vectorized equivalent
- Calling external functions per row that can't be lifted to array ops
- Profile with `%timeit` — if slow, rewrite as `np.select` or element-wise

---

## Chunked I/O for Large Files

### Read in Chunks

```python
chunk_size = 100_000
chunks = []

for chunk in pd.read_csv('large.csv', chunksize=chunk_size):
    processed = chunk[chunk['value'] > 0]                       # Filter
    processed = processed.groupby('category')['value'].sum()    # Aggregate
    chunks.append(processed)

result = pd.concat(chunks).groupby(level=0).sum()
```

### Reusable Chunk Processor

```python
def process_large_csv(
    filepath: str,
    chunk_size: int = 100_000,
    filter_func=None,
    agg_func=None,
) -> pd.DataFrame:
    results = []
    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        if filter_func:
            chunk = filter_func(chunk)
        if agg_func:
            chunk = agg_func(chunk)
        results.append(chunk)
    return pd.concat(results)
```

### Read Only Needed Columns

```python
# Skip columns at read time — never load what you don't need
df = pd.read_csv('file.csv', usecols=['id', 'value', 'category'])

# Specify dtypes at read time — avoids post-load conversion cost
df = pd.read_csv('file.csv', dtype={'id': 'Int32', 'category': 'category'})
```
