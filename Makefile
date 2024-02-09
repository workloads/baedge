# Makefile for Baedge Server

# configuration
TITLE  = 🎫 BAEDGE SERVER

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
		baedge.py baedge_server.py
