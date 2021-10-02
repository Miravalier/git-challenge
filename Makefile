DOMAIN = git.challenge.local

.PHONY: help nginx docker create_api_user delete_api_user deps

help:
	@echo "make help"
	@echo "  Display this message"
	@echo
	@echo "make docker"
	@echo "  Start the containers"
	@echo
	@echo "sudo make nginx"
	@echo "  Serve the application on the domain $(DOMAIN)"
	@echo
	@echo "make create_api_user"
	@echo "  Create a new admin user with the username 'challenge_api',"
	@echo "  then put that user's access token into .env and restart"
	@echo "  the docker container"
	@echo
	@echo "make delete_api_user"
	@echo "  Delete the 'challenge_api' user"
	@echo
	@echo "make deps"
	@echo "  List the dependencies needed for this Makefile"

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

create_api_user:
	@TOKEN="$$(docker-compose exec gitea su git -c \
		"gitea admin user create --username challenge_api --admin --access-token --email challenge_api@$(DOMAIN) --random-password" \
		| grep -Eo "[a-fA-F0-9]{40,120}")" && \
		sed -Ei "s/GITEA_TOKEN=.*/GITEA_TOKEN=$$TOKEN/g" .env
	@echo "User 'challenge_api' created"
	docker-compose rm -fsv challenge
	docker-compose up -d challenge
	@echo "Container restarted"

delete_api_user:
	docker-compose exec gitea su git -c "gitea admin user delete --username challenge_api"

deps:
	@echo "python3\ndocker\ndocker-compose\nnginx\nsed"
