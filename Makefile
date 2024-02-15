# Makefile for Baedge Server

# configuration
TITLE          = 🎫 {BA,E}DGE SERVER
BINARY_PYTHON ?= python3
FLAKE_CONFIG  ?= ".flake8"
FLASK_APP     ?= server
FLASK_PORT    ?= 2343
NOMAD_SERVICE ?= "baedge-main"
PYLINT_RCFILE ?= ".pylintrc"

# retrieve Baedge Server API information from Nomad
BAEDGE_API = $(shell nomad service info -t '{{range .}}{{printf "http://%s:%v\n" .Address .Port }}{{end}}' "${NOMAD_SERVICE}")

include ../tooling/make/configs/shared.mk
include ../tooling/make/functions/shared.mk
include ../tooling/make/targets/shared.mk

.SILENT .PHONY: deps
deps: # install dependencies [Usage: `make deps`]
	pip \
		install \
		--requirement "requirements.txt"

.SILENT .PHONY: deps-dev
deps-dev: # install development dependencies [Usage: `make deps-dev`]
	pip \
		install \
		--requirement "requirements-dev.txt"

.SILENT .PHONY: fix
fix: # fix Python files using autopep8 [Usage: `make fix`]
	autopep8 \
		--in-place \
		*.py \

.SILENT .PHONY: lint
lint: # lint Python files using Flake8 and Pylint [Usage: `make lint`]
	flake8 \
		--config="${FLAKE_CONFIG}" \
		*.py \
	&& \
	pylint \
		--rcfile="${PYLINT_RCFILE}" \
		*.py

.SILENT .PHONY: snyk
snyk: # check Python files using Snyk [Usage: `make snyk`]
	snyk \
		test \
			--command="${BINARY_PYTHON}" \
			--file="requirements.txt" \
			--package-manager=pip \
			-- --allow-missing

.SILENT .PHONY: routes
routes: # list Baedge Server routes using Flask [Usage: `make routes`]
	flask \
		--app="${FLASK_APP}" \
		routes

.SILENT .PHONY: run
run: # run Baedge Server using Flask [Usage: `make run`]
	flask \
		--app="${FLASK_APP}" \
		--debug \
		run \
			--port="${FLASK_PORT}"

.SILENT .PHONY: env-info
env-info: # print Baedge Environment information [Usage: `make env-info`]
	env | \
	grep \
		"BAEDGE_"

.SILENT .PHONY: gpio-info
gpio-info: # print GPIO information using Python [Usage: `make gpio-info`]
	${BINARY_PYTHON} \
		gpio.py

.SILENT .PHONY: screen
screen: # set Baedge Screen [Usage: `make screen screen=<screen>`]
	$(if $(screen),,$(call missing_argument,screen=<screen>))

	echo "Attempting to write screen \`${screen}\` on device...\n"

	curl \
		--location \
		--request POST \
  	"${BAEDGE_API}/v1/device/write" \
		--form "screen=\"$(screen)\""
