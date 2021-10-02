DOMAIN = git.challenge.local

.PHONY: help nginx docker

help:
	@echo "make help"
	@echo "  Display this message."
	@echo
	@echo "make docker"
	@echo "  Start the containers."
	@echo
	@echo "sudo make nginx"
	@echo "  Serve the application on the domain $(DOMAIN)"

SITE_AVAILABLE := /etc/nginx/sites-available/$(DOMAIN)
SITE_ENABLED := /etc/nginx/sites-enabled/$(DOMAIN)
RAND_OCTET=$(shell python3 -c 'import secrets; print(secrets.randbelow(256))')
nginx:
	@rm -f "$(SITE_ENABLED)"
	@if [ -z "$$(grep "$(DOMAIN)" /etc/hosts)" ]; then \
			echo "127.$(RAND_OCTET).$(RAND_OCTET).$(RAND_OCTET) $(DOMAIN)" >> /etc/hosts; \
		fi
	cp nginx.site "$(SITE_AVAILABLE)"
	. ./.env; sed -i "s/{GITEA_HTTP_PORT}/$$GITEA_HTTP_PORT/" "$(SITE_AVAILABLE)"
	. ./.env; sed -i "s/{GITEA_CHALLENGE_HTTP_PORT}/$$GITEA_CHALLENGE_HTTP_PORT/" "$(SITE_AVAILABLE)"
	sed -i "s/{DOMAIN}/$(DOMAIN)/" "$(SITE_AVAILABLE)"
	ln -s "$(SITE_AVAILABLE)" "$(SITE_ENABLED)"
	service nginx restart
	@echo "Gitea reachable at http://$(DOMAIN)/"
	@echo "Challenge reachable at http://$(DOMAIN)/challenge"

docker:
	docker-compose down
	docker-compose build
	docker-compose up -d
