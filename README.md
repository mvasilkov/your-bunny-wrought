# Your Bunny Wrought

<img src="https://raw.githubusercontent.com/mvasilkov/your-bunny-wrought/master/fluff/bunny.jpeg" height="256" width="256">

[_Your Bunny Wrought_][git] (_but_ for short) is a collection of scripts
related to file formats and compression.

[git]: https://github.com/mvasilkov/your-bunny-wrought

## Installation

```bash
pip install but
```

## CLI Usage

```
but serve_static [-h HOST] [-p PORT] [DIR]

    Alias: server

but render_template [-t TEMPLATE_DIR] PATTERN [PATTERN ...]

    Alias: template

but run_script SCRIPT

    Alias: run
```

### Watching for Changes

```
but watch_files DEF_FILE

    Alias: watch
```

DEF_FILE is a JSON definition file with the following structure:

```json
{
  "paths": ["."],
  "handlers": [
    {
      "patterns": ["**/*.py"],
      "script": ["echo", "File changed:", "{file}"]
    }
  ]
}
```

### External Executables

```
but ffmpeg -- [ARGS]
but tsc -- [ARGS]
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
