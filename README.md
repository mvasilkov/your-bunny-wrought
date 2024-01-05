# Your Bunny Wrought

[_Your Bunny Wrought_][git] (_but_ for short) is a collection of scripts
related to file formats and compression.

[git]: https://github.com/mvasilkov/your-bunny-wrought

## Installation

```bash
pip install but
```

## Usage

```
but serve_static [-h HOST] [-p PORT] [DIR]

but render_template [-t TEMPLATE_DIR] PATTERN [PATTERN ...]
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
pip wheel --no-deps .
twine upload but-*-py3-none-any.whl
rm -r build/ but.egg-info/ but-*-py3-none-any.whl
```
