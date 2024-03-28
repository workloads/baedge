# Makefile for Baedge Server

# configuration
BAEDGE_API      = $(shell $(BINARY_NOMAD) service info -t '{{range .}}{{printf "http://%s:%v\n" .Address .Port }}{{end}}' "${NOMAD_SERVICE}")
BINARY_FLASK   ?= flask
FLASK_APP      ?= server
FLASK_PORT     ?= 2343
NOMAD_SERVICE  ?= "baedge-main"
MAKEFILE_TITLE  = 🎫 {BA,E}DGE SERVER


include ../tooling/make/configs/shared.mk
include ../tooling/make/functions/shared.mk
include ../tooling/make/targets/python.mk
include ../tooling/make/functions/snyk.mk
include ../tooling/make/targets/shared.mk

.SILENT .PHONY: routes
routes: # list Baedge Server routes using Flask [Usage: `make routes`]
	$(BINARY_FLASK) \
		--app="${FLASK_APP}" \
		routes

.SILENT .PHONY: run
run: # run Baedge Server using Flask [Usage: `make run`]
	$(BINARY_FLASK) \
		--app="${FLASK_APP}" \
		--debug \
		run \
			--port="${FLASK_PORT}"

.SILENT .PHONY: env
env: # print environment information [Usage: `make env-info`]
	$(call print_env,"BAEDGE_")

.SILENT .PHONY: gpio-info
gpio-info: # print GPIO information using Python [Usage: `make gpio-info`]
	$(BINARY_PYTHON) \
		gpio.py

.SILENT .PHONY: screen
screen: # set Baedge Screen [Usage: `make screen screen=<screen>`]
	$(if $(screen),,$(call missing_argument,screen=<screen>))

	$(call print_reference,"Attempting to write screen \`${screen}\` on device...\n")

	$(BINARY_CURL) \
		--location \
		--request POST \
  	"${BAEDGE_API}/v1/device/write" \
		--form "screen=\"$(screen)\""

.SILENT .PHONY: snyk
snyk: # check Python files using Snyk [Usage: `make snyk`]
	$(call snyk_test,$(BINARY_PYTHON),$(CONFIG_PIP_REQS),pip,"--allow-missing")
	$(call snyk_test,$(BINARY_PYTHON),$(CONFIG_PIP_REQS_DEV),pip,"--allow-missing")
