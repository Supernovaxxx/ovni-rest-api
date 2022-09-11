# Development management facilities
#
# This file specifies useful routines to streamline development management.
# See https://www.gnu.org/software/make/.


# Consume environment variables
ifneq (,$(wildcard .env))
	include .env
endif

# Tool configuration
SHELL := /bin/bash
GNUMAKEFLAGS += --no-print-directory

# Path record
ROOT_DIR ?= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SOURCE_DIR ?= $(ROOT_DIR)/src
SERVICE_DIR ?= $(SOURCE_DIR)/$(SERVICE)

# Target files
ENV_FILE ?= .env
EPHEMERAL_ARCHIVES ?=

# Executables definition
GIT ?= git

# Behavior configuration
SERVICE_URL ?= http://localhost:$(PORT)
SERVICE ?= service
PORT ?= 8000


%: # Treat unrecognized targets
	@ printf "\033[31;1mUnrecognized routine: '$(*)'\033[0m\n"
	$(MAKE) help

help:: ## Show this help
	@ printf "\033[33;1mGNU-Make available routines:\n"
	egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[37;1m%-20s\033[0m %s\n", $$1, $$2}'

prepare:: ## Inicialize virtual environment
	test -r $(ENV_FILE) || cp --froce $(ENV_FILE).example $(ENV_FILE)

init:: veryclean prepare ## Configure development environment
	test -r '.gitmodules' && $(GIT) submodule update --init --recursive

execute:: setup run ## Setup and Run application

setup:: finish ## Process source code into an executable program

run:: ## Launch application locally
	docker run \
		--name $(SERVICE) \
		--hostname $(SERVICE) \
		--publish $(PORT):$(PORT) \
		--workdir /$(SERVICE) \
		--volume $(SERVICE_DIR):/$(SERVICE) \
 		--env-file $(ENV_FILE) \
		--health-cmd 'curl $(SERVICE_URL) || exit 1' \
		--interactive \
		--tty \
		python:3.10 \
		bash -c 'make init && make setup && make run'

finish:: ## Stop application execution
	docker exec $(SERVICE) bash -c 'make finish'
	docker stop $(SERVICE)

bash::
	docker exec \
		--env-file $(ENV_FILE) \
		--interactive \
		--tty \
		$(SERVICE) \
		bash

show::
	@docker logs --tail 10 $(SERVICE)
	echo
	docker ps \
		--filter name=$(SERVICE) \
		--format 'table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Networks}}\t{{.State}}\t{{.Status}}\t{{.Command}}' \
		--all
	echo
	docker stats --no-stream $(SERVICE)

check:: ## Output application status
	curl $(SERVICE_URL)

open:: ## Browse application
	xdg-open $(SERVICE_URL)

test:: ## Verify application's behavior requirements completeness

build:: clean ## Build application running environment
	docker build \
		--file $(SERVICE_DIR)/Dockerfile \
		--tag $(SERVICE) \
		--add-host $(SERVICE):127.0.0.1 \
		--pull \
		--force-rm \
		$(SERVICE_DIR)

publish:: build ## Upload application container to registry

deploy:: build ## Deploy application

clean:: ## Delete project ephemeral archives
	-rm -fr $(EPHEMERAL_ARCHIVES)

veryclean:: stop clean ## Delete all generated files
	-docker image rm $(SERVICE)


.EXPORT_ALL_VARIABLES:
.ONESHELL:
.PHONY: help prepare init execute setup run finish bash show check open test build publish deploy clean veryclean
