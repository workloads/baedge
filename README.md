# {Ba,E}dge Computing Server

> Python-based server for {Ba,E}dge Computing.

## Table of Contents

<!-- TOC -->
* [{Ba,E}dge Computing Server](#baedge-computing-server)
  * [Table of Contents](#table-of-contents)
  * [Requirements](#requirements)
    * [Hardware](#hardware)
    * [Software](#software)
      * [Development](#development)
  * [Usage](#usage)
  * [Contributors](#contributors)
  * [License](#license)
<!-- TOC -->

## Requirements

### Hardware

- [Raspberry Pi Zero 2W](https://www.raspberrypi.org/products/raspberry-pi-zero-2-w/)
- Waveshare eInk display
  - [2.13 inch display](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(B))
  - (preferred) [2.7 inch display](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT_(B))
  - [2.9 inch display](https://www.waveshare.com/wiki/2.9inch_e-Paper_Module_(B))

### Software

See [requirements.txt](./requirements.txt) for a list of Python dependencies.

#### Development

For development and testing of this repository:

- `flake8` `7.0.0` or [newer](https://pypi.org/project/flake8/)
- `pylint` `3.0.0` or [newer](https://pypi.org/project/pylint/)

These dependencies can be installed using the following command:

```shell
make deps-dev
```

## Usage

This repository provides a [Makefile](./Makefile)-based workflow.

Running `make` without commands will print out the following help information:

```text
🎫 {BA,E}DGE SERVER

Target          Description                                   Usage
deps            install dependencies                          `make deps`
deps-dev        install development dependencies              `make deps-dev`
fix             fix Python files using autopep8               `make fix`
lint            lint Python files using Flake8 and Pylint     `make lint`
snyk            check Python files using Snyk                 `make snyk`
routes          list Baedge Server routes using Flask         `make routes`
run             run Baedge Server using Flask                 `make run`
env-info        print Baedge Environment information          `make env-info`
gpio-info       print GPIO information using Python           `make gpio-info`
screen          set Baedge Screen                             `make screen screen=<screen>`
help            display a list of Make Targets                `make help`
_listincludes   list all included Makefiles and *.mk files    `make _listincludes`
_selfcheck      lint Makefile                                 `make _selfcheck`
```

## Contributors

For a list of current (and past) contributors to this repository, see [GitHub](https://github.com/workloads/baedge-server/graphs/contributors).

## License

Licensed under the Apache License, Version 2.0 (the "License").

You may download a copy of the License at [apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0).

See the License for the specific language governing permissions and limitations under the License.
