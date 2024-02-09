# Makefile for Baedge Server

# configuration
TITLE     = 🎫 BAEDGE SERVER
FLASK_APP = baedge_server
FLASK_PORT = 2343

include ../tooling/make/configs/shared.mk
include ../tooling/make/targets/shared.mk

.SILENT .PHONY: deps
deps: # install PIP dependencies [Usage: `make deps`]
	pip \
		install \
		-r "requirements.txt"

.SILENT .PHONY: lint
lint: # lint Python files using Pylint [Usage: `make lint`]
	pylint \
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
		run \
			--debug \
			--port="${FLASK_PORT}"

