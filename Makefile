# Makefile for Baedge Server

# configuration
TITLE         = 🎫 BAEDGE SERVER
FLAKE_CONFIG ?= ".flake8"
FLASK_APP    ?= baedge_server
FLASK_PORT   ?= 2343

include ../tooling/make/configs/shared.mk
include ../tooling/make/targets/shared.mk

.SILENT .PHONY: deps
deps: # install dependencies [Usage: `make deps`]
	pip \
		install \
		-r "requirements.txt"

.SILENT .PHONY: deps-dev
deps-dev: # install development dependencies [Usage: `make deps-dev`]
	pip \
		install \
		-r "requirements-dev.txt"

.SILENT .PHONY: lint
lint: # lint Python files using Pylint [Usage: `make lint`]
	pylint \
		*.py \
	&& \
	flake8 \
		--config="${FLAKE_CONFIG}" \
		*.py

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
