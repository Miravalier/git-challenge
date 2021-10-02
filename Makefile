.PHONY: help nginx docker

help:
	@echo "make help, make docker, sudo make nginx"

SITE_AVAILABLE := /etc/nginx/sites-available/git.challenge.local
SITE_ENABLED := /etc/nginx/sites-enabled/git.challenge.local
nginx:
	@rm -f $(SITE_ENABLED)
	@if [ -z "$$(grep "git.challenge.local" /etc/hosts)" ]; then \
			echo "127.0.5.5 git.challenge.local" >> /etc/hosts; \
		fi
	cp nginx.site $(SITE_AVAILABLE)
	. ./.env; sed -i "s/{GITEA_HTTP_PORT}/$$GITEA_HTTP_PORT/" $(SITE_AVAILABLE)
	. ./.env; sed -i "s/{GITEA_CHALLENGE_HTTP_PORT}/$$GITEA_CHALLENGE_HTTP_PORT/" $(SITE_AVAILABLE)
	ln -s $(SITE_AVAILABLE) $(SITE_ENABLED)
	service nginx restart
	@echo "Gitea reachable at http://git.challenge.local/"
	@echo "Challenge reachable at http://git.challenge.local/challenge/"

docker:
	docker-compose down
	docker-compose build
	docker-compose up -d
