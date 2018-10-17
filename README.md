# chpl-magic

IPython cell magic for chapel code.

## Quick Start
Install with pip:
```bash
pip install git+https://github.com/reuster986/chpl-magic
```

In Jupyter:
```python
%load_ext chpl_magic
```

```python
%%chpl
export proc addem(x:int, y:int):int {
    return x + y;
}
```

```python
addem(2, 3) # prints 5
```

## Dependencies
* Chapel >= 1.18 compiled in "shared" mode (with CHPL_LIBMODE=shared)
* python3
* Cython
* numpy

Uses Chapel's [compiler utility](https://chapel-lang.org/docs/technotes/libraries.html#using-your-library-in-python) for exporting libraries to Python.