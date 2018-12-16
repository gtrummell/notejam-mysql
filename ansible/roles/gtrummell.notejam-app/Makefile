.PHONY: help
.DEFAULT_GOAL := help

# Self-documenting makefile compliments of François Zaninotto http://bit.ly/2PYuVj1

help:
	@echo "Make targets for NoteJam MySQL:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

get-deps: ## Retrieve dependent Docker containers before containerized testing
	@tar czf ./files/notejam-mysql.tgz ../../../notejam
	@docker pull ubuntu:18.04
	@ansible-galaxy install -c -r ./requirements.yml

clean: ## Sanitize the workspace by removing node modules, containers, etc.
	@rm -rf ./notejam-mysql.tgz
	@for role_dep in $(shell grep "^- src:" requirements.yml | sed 's/^-\ src\:\ //g') ; do \
		rm -rf ../$$role_dep ; \
	done
	@for role_dep in $(shell grep "^- src:" requirements.yml | sed 's/^-\ src\:\ //g') ; do \
		rm -rf ~/.ansible/roles/$$role_dep ; \
	done

test: clean get-deps  ## Test the code needed to build a Docker images for the application
	@molecule test
