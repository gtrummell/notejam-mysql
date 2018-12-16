.PHONY: help
.DEFAULT_GOAL := help

export NOTEJAM_VERSION := $(shell jq -r '.version' notejam/package.json)
export TF_VAR_notejam_version := $(shell jq -r '.version' notejam/package.json)


# Self-documenting makefile compliments of François Zaninotto http://bit.ly/2PYuVj1

help:
	@echo "Make targets for NoteJam MySQL:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build-ami: test-ami ## Build an Amazon EC2 AMI for the application
	@packer build packer-notejam-ec2.json

build-container: test-container ## Test the code needed to build a Docker images for the application
	@docker build . -t notejam-app:${NOTEJAM_VERSION} -t notejam-app:latest

build-stack-aws: test-stack-aws ## Build a complete application stack in Amazon AWS EC2/RDS using Terraform
	@cd terraform && $(MAKE) build-stack-aws

build-stack-docker: test-stack-docker ## Build a complete application stack using Docker (testing only)
	@docker-compose up -d

ci: test-container test-ami test-stack-docker validate-stack-aws ## Run all tests

global-clean: ## Sanitize the workspace by removing node modules, containers, etc.
	@docker-compose stop
	@docker-compose rm -f
	@docker rmi -f notejam-app:${NOTEJAM_VERSION}
	@rm -rf ./notejam/node_modules ./notejam/wait-for-it.sh ./terraform/.terraform
	@find ./ -type f -name *.retry -exec rm -f {} \;
	@for ansible_role_dir in $(find ./ansible/roles/ -maxdepth 1 -type d ! -name gtrummell.notejam-app | tail -n +2) ; do \
		rm -rf $$ansible_role_dir ; \
    done

global-getdeps: ## Retrieve dependencies locally
	@docker pull gtrummell/iac-testkit-ubuntu:18.04 | cat
	@docker pull hadolint/hadolint:latest | cat
	@docker pull mysql:5.7 | cat
	@docker pull node:10.13.0 | cat
	@docker pull sdesbure/yamllint:latest | cat
	@docker pull sahsu/docker-jsonlint:latest | cat
	@docker pull ubuntu:18.04 | cat
	@pip install --upgrade -r requirements.txt

rm-stack-aws: ## Tear down the AWS stack using Terraform
	@cd terraform && $(MAKE) rm-stack-aws

rm-stack-docker: ## Tear down the Docker stack
	@docker-compose stop
	@docker-compose rm -f

test-ami: global-clean global-getdeps ## Test the code needed to build an EC2 AMI for the application
	@cd ./ansible/roles/gtrummell.notejam-app && $(MAKE) test
	@docker run -v ${PWD}:/jsonlint --rm sahsu/docker-jsonlint jsonlint -q /jsonlint/packer-notejam-ec2.json
	@packer inspect packer-notejam-ec2.json
	@packer validate packer-notejam-ec2.json

test-app: global-clean global-getdeps ## Test the application locally
	@docker-compose up -d db
	@cd notejam && ./node_modules/mocha/bin/mocha tests

test-container: global-clean global-getdeps ## Test the code needed to build a Docker images for the application
	@echo "Testing ./Dockerfile with Hadolint (no news is good news)..."
	@docker run --rm -i hadolint/hadolint < Dockerfile

test-stack-aws: ## Test a complete application stack in Amazon AWS EC2/RDS using Terraform
	@cd terraform && $(MAKE) test-stack-aws

test-stack-docker: ## Test a complete application stack using Docker
	@docker run -v ${PWD}:/yaml --rm sdesbure/yamllint:latest yamllint -d relaxed /yaml/docker-compose-buildtime.yml /yaml/docker-compose-image.yml
	@docker-compose -f docker-compose-buildtime.yml config
	@docker-compose -f docker-compose-image.yml config

validate-stack-aws: ## Validate a complete application stack for Amazon AWS EC2/RDS using Terraform
	@cd terraform && $(MAKE) validate-stack-aws
