.PHONY: help
.DEFAULT_GOAL := help

# Self-documenting makefile compliments of François Zaninotto http://bit.ly/2PYuVj1

help:
	@echo "Make targets for NoteJam MySQL:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build-stack-aws: test-stack-aws ## Build a complete application stack in Amazon AWS EC2/RDS using Terraform
	@docker run -it -v $(PWD):/terraform gtrummell/iac-testkit-ubuntu:18.04 "cd /terraform && terraform apply"

get-deps: ## Get toolchain dependencies
	@docker pull gtrummell/iac-testkit-ubuntu:18.04

init-clean: ## Sanitize the workspace by removing modules, temp files, etc.
	@rm -rf ./.terraform

state-clean: ## Clean existing Terraform state
	@rm -rf ./terraform.tfstate ./terraform.tfstate.backup

init: ## Initialize Terraform and dependencies
	@docker run -it -v $(PWD):/terraform gtrummell/iac-testkit-ubuntu:18.04 "cd /terraform && terraform init"

rm-stack-aws: init ## Tear down the AWS stack using Terraform
	@docker run -it -v $(PWD):/terraform gtrummell/iac-testkit-ubuntu:18.04 "cd /terraform && terraform destroy"

test-stack-aws: init validate ## Test a complete application stack in Amazon AWS EC2/RDS using Terraform
	@docker run -it -v $(PWD):/terraform gtrummell/iac-testkit-ubuntu:18.04 "cd /terraform && terraform plan"

validate-stack-aws: init ## Validate a complete application stack for Amazon AWS EC2/RDS using Terraform
	@docker run -it -v $(PWD):/terraform gtrummell/iac-testkit-ubuntu:18.04 "cd /terraform && terraform validate"
