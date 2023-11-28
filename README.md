# Your Bunny Wrought

[_Your Bunny Wrought_][git] (_but_ for short) is a collection of scripts
related to file formats and compression.

[git]: https://github.com/mvasilkov/your-bunny-wrought

## Installation

```bash
pip install but
```

## Working on Your Bunny Wrought

```bash
python3.12 -m venv virtual
. ./virtual/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
```

### Uploading to PyPI

```bash
pip wheel .
twine upload but-*-py3-none-any.whl
```
