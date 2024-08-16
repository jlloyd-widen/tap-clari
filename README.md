# tap-clari

`tap-clari` is a Singer tap for Clari.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

<!--

Developer TODO: Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

## Installation

Install from PyPi:

```bash
pipx install tap-clari
```
-->

Install from GitHub:

```bash
pipx install git+https://github.com/jlloyd-widen/tap-clari.git@main
```


## Configuration

### Accepted Config Options

<!--

This section can be created by copy-pasting the CLI output from:

```
tap-clari --about --format=markdown
```
-->

| Setting | Required | Default | Description                                                                                                                                                                                                                                              |
|:--------|:--------:|:-------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| api_key |   True   |  None   | The token to authenticate against the Clari API                                                                                                                                                                                                          |
| time_period |  False   |  None   | Fiscal Quarter for when you'd like to run your export. Must be passed in as a string (e.g. 'YYYY_QQ'). Defaults to the current quarter.                                                                                                                  |
| forecast_ids |  False   |  []   | An array of IDs of the Forecast Tabs you would like to export data from.                                                                                                                                                                                 |
| opp_ids |  False   |   []    | An array of IDs of the opportunities for extraction.                                                                                                                                                                                                                                                         |
| stream_maps |  False   |  None   | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html).                                                                                                              |
| stream_map_config |  False   |  None   | User-defined config values to be used within map expressions.                                                                                                                                                                                            |
| faker_config |  False   |  None   | Config for the [`Faker`](https://faker.readthedocs.io/en/master/) instance variable `fake` used within map expressions. Only applicable if the plugin specifies `faker` as an addtional dependency (through the `singer-sdk` `faker` extra or directly). |
| faker_config.seed |  False   |  None   | Value to seed the Faker generator for deterministic output: https://faker.readthedocs.io/en/master/#seeding-the-generator                                                                                                                                |
| faker_config.locale |  False   |  None   | One or more LCID locale strings to produce localized output for: https://faker.readthedocs.io/en/master/#localization                                                                                                                                    |
| flattening_enabled |  False   |  None   | 'True' to enable schema flattening and automatically expand nested properties.                                                                                                                                                                           |
| flattening_max_depth |  False   |  None   | The max depth to flatten schemas.                                                                                                                                                                                                                        |
| batch_config |  False   |  None   |                                                                                                                                                                                                                                                          |
| batch_config.encoding |  False   |  None   | Specifies the format and compression of the batch files.                                                                                                                                                                                                 |
| batch_config.encoding.format |  False   |  None   | Format to use for batch files.                                                                                                                                                                                                                           |
| batch_config.encoding.compression |  False   |  None   | Compression format to use for batch files.                                                                                                                                                                                                               |
| batch_config.storage |  False   |  None   | Defines the storage layer to use when writing batch files                                                                                                                                                                                                |
| batch_config.storage.root |  False   |  None   | Root path to use when writing batch files.                                                                                                                                                                                                               |
| batch_config.storage.prefix |  False   |  None   | Prefix to use when writing batch files.                                                                                                                                                                                                                  |


A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-clari --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

Please note that you cannot select or deselect the `forecast` streams using the `select` configuration optionn. Not providing any `forecast_ids` will result in the same behavior as deselecting the `forecast` stream.

### Source Authentication and Authorization

<!--
Developer TODO: If your tap requires special access on the source system, or any special authentication requirements, provide those here.
-->

## Usage

You can easily run `tap-clari` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-clari --version
tap-clari --help
tap-clari --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-clari` CLI interface directly using `poetry run`:

```bash
poetry run tap-clari --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-clari
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-clari --version
# OR run a test `elt` pipeline:
meltano elt tap-clari target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
