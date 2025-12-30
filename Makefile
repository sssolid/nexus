# ============================================================
# Crown Nexus — Full Master Makefile
# ============================================================

SHELL := bash
.DEFAULT_GOAL := help
.ONESHELL:
.SILENT:

# ============================================================
# HARD SAFETY GUARD
# ============================================================
# GNU Make executes all goals; forbid multi-goal invocation.
# ============================================================

ifneq ($(words $(MAKECMDGOALS)),1)
  $(error Invalid usage. Run exactly ONE target at a time. Use 'make help'.)
endif

# ============================================================
# User-facing knobs
# ============================================================

ENV     ?= dev        # dev | prod
ARGS    ?=
CMD     ?=
FILE    ?=
SERVICE ?= web

# ============================================================
# Docker / Compose configuration
# ============================================================

COMPOSE := docker compose

BASE_FILES := -f docker-compose.yml
DEV_FILES  := $(BASE_FILES) -f docker-compose.dev.yml
PROD_FILES := $(BASE_FILES) -f docker-compose.prod.yml

DEV_ENV_FILE  := .env.development
PROD_ENV_FILE := .env.production

WEB     := web
DB      := db
REDIS   := redis
WORKER  := celery_worker
BEAT    := celery_beat
FLOWER  := flower

ifeq ($(ENV),prod)
	COMPOSE_FILES := $(PROD_FILES)
	ENV_FILE := $(PROD_ENV_FILE)
	IS_PROD := 1
else
	COMPOSE_FILES := $(DEV_FILES)
	ENV_FILE := $(DEV_ENV_FILE)
	IS_PROD := 0
endif

# ============================================================
# Helpers
# ============================================================

define require_file
	if [[ ! -f "$(1)" ]]; then
		echo "ERROR: Missing required file: $(1)"
		exit 1
	fi
endef

define confirm
	read -p "$(1) (yes/no): " confirm
	[[ "$$confirm" == "yes" ]] || exit 1
endef

define confirm_prod
	if [[ "$(IS_PROD)" == "1" ]]; then
		$(call confirm,$(1))
	fi
endef

define dc
	export ENV_FILE="$(ENV_FILE)"
	$(COMPOSE) $(COMPOSE_FILES) $(1)
endef

define exec
	$(call dc,exec $(1) $(2))
endef

define manage
	$(call exec,$(WEB),python manage.py $(1))
endef

define manage-local
	python manage.py $(1)
endef

# ============================================================
# HELP — LEVEL 1 (CATEGORIES)
# ============================================================

help:
	@echo ""
	@echo "Crown Nexus — Help"
	@echo ""
	@echo "Categories:"
	@echo "  docker     Container lifecycle"
	@echo "  shells     Interactive shells"
	@echo "  django     Django management"
	@echo "  wagtail    Wagtail CMS"
	@echo "  celery     Background workers"
	@echo "  media      Media & thumbnails"
	@echo "  data       ACES / PIES / sync"
	@echo "  database   Database operations"
	@echo "  formatting Formatting & linting"
	@echo "  git        Git workflows"
	@echo "  pip        Pip workflows"
	@echo "  bundles    Multi-step workflows"
	@echo "  shemas     Generate aces/pies schemas"
	@echo ""
	@echo "Usage:"
	@echo "  make help-<category>"
	@echo "  make help-<command>"
	@echo ""

# ============================================================
# HELP — LEVEL 2 (CATEGORIES)
# ============================================================

help-docker:
	@echo "Docker commands:"
	@echo "  up            Start containers"
	@echo "  down          Stop containers"
	@echo "  restart       Restart containers"
	@echo "  ps            Show container status"
	@echo "  logs          Tail logs"

help-shells:
	@echo "Shell commands:"
	@echo "  shell         Bash shell in web container"
	@echo "  exec          Run command in container"
	@echo "  psql          PostgreSQL shell"
	@echo "  redis-cli     Redis shell"

help-django:
	@echo "Django commands:"
	@echo "  manage            Run manage.py command"
	@echo "  migrate           Apply migrations"
	@echo "  makemigrations    Create migrations"
	@echo "  superuser         Create superuser"
	@echo "  collectstatic     Collect static files"
	@echo "  check             System checks"
	@echo "  check-deploy      Production checks"
	@echo "  shell-plus        Django shell_plus"
	@echo "  show-urls         List URL patterns"
	@echo "  diffsettings      Show settings diff"
	@echo "  test              Run tests"

help-wagtail:
	@echo "Wagtail commands:"
	@echo "  wagtail-init      Bootstrap Wagtail"
	@echo "  update-index      Update search index"
	@echo "  rebuild-index     Rebuild search index"

help-celery:
	@echo "Celery commands:"
	@echo "  celery-active     Active tasks"
	@echo "  celery-queues     Queue info"
	@echo "  celery-purge      Purge queues"

help-media:
	@echo "Media commands:"
	@echo "  thumbs-clear      Clear thumbnails"
	@echo "  thumbs-rebuild    Rebuild thumbnails"

help-data:
	@echo "Data commands:"
	@echo "  aces-import       Import ACES XML"
	@echo "  pies-import       Import PIES XML"
	@echo "  sync-all          Run all syncs"

help-database:
	@echo "Database commands:"
	@echo "  db-backup         Backup database"
	@echo "  db-restore        Restore database"
	@echo "  db-reset          Reset DEV database"

help-formatting:
	@echo "Formatting commands:"
	@echo "  format            Black + Ruff"
	@echo "  format-check      Check formatting"
	@echo "  lint              Run linters"

help-git:
	@echo "Git commands:"
	@echo "  git-status        Git status"
	@echo "  git-sync          Fetch + rebase"
	@echo "  git-clean         Remove untracked files"

help-pip:
	@echo "Pip commands:"
	@echo "  pip-compile       Compile requirements"

help-bundles:
	@echo "Bundle commands:"
	@echo "  dev               Bootstrap dev environment"
	@echo "  doctor            Environment diagnostics"

# ============================================================
# DOCKER
# ============================================================

up:
	$(call require_file,$(ENV_FILE))
	$(call confirm_prod,Start PRODUCTION containers?)
	$(call dc,up $(ARGS))

help-up:
	@echo "up — Start Docker containers"
	@echo "Usage: make up [ENV=dev|prod] [ARGS='-d --build']"

down:
	$(call confirm_prod,Stop PRODUCTION containers?)
	$(call dc,down $(ARGS))

help-down:
	@echo "down — Stop Docker containers"

restart:
	$(MAKE) down ENV=$(ENV)
	$(MAKE) up ENV=$(ENV)

help-restart:
	@echo "restart — Restart containers"

ps:
	$(call dc,ps)

help-ps:
	@echo "ps — Show container status"

logs:
	$(call dc,logs -f --tail=200 $(ARGS))

help-logs:
	@echo "logs — Tail logs (ARGS=service)"

# ============================================================
# SHELLS
# ============================================================

shell:
	$(call exec,$(WEB),bash)

help-shell:
	@echo "shell — Bash shell in web container"

exec:
	$(call exec,$(SERVICE),$(CMD))

help-exec:
	@echo "exec — Run command in container"
	@echo "Usage: make exec SERVICE=web CMD='bash'"

psql:
	$(call exec,$(DB),psql -U $$DB_USER $$DB_NAME)

help-psql:
	@echo "psql — PostgreSQL shell"

redis-cli:
	$(call exec,$(REDIS),redis-cli -a $$REDIS_PASSWORD)

help-redis-cli:
	@echo "redis-cli — Redis shell"

# ============================================================
# DJANGO
# ============================================================

manage:
	$(call manage,$(CMD))

help-manage:
	@echo "manage — Run Django management command"
	@echo "Usage: make manage CMD='migrate'"

migrate:
	$(call manage,migrate)

help-migrate:
	@echo "migrate — Apply migrations"

makemigrations:
	$(call manage-local,makemigrations)

help-makemigrations:
	@echo "makemigrations — Create migrations"

makemigrations-web:
	$(call manage,makemigrations)

help-makemigrations-web:
	@echo "makemigrations — Create migrations"

.PHONY: migrations-nuke
migrations-nuke:
	@if [[ "$(IS_PROD)" == "1" ]]; then \
		echo "ERROR: Refusing to delete migrations in production."; \
		exit 1; \
	fi
	$(call confirm,This will DELETE ALL Django migration files (except __init__.py) in DEV. Continue?)
	echo "Deleting migration files..."
	find . \
		-path "./.venv" -prune -o \
		-path "./venv" -prune -o \
		-path "*/migrations/*.py" \
		! -name "__init__.py" \
		-type f \
		-exec rm -f {} +
	echo "Migration files deleted."

help-migrations-nuke:
	@echo "migrations-nuke — Delete ALL migration files (DEV ONLY, destructive)"

superuser:
	$(call manage,createsuperuser)

help-superuser:
	@echo "superuser — Create Django superuser"

collectstatic:
	$(call manage,collectstatic --noinput)

help-collectstatic:
	@echo "collectstatic — Collect static files"

check:
	$(call manage,check)

help-check:
	@echo "check — Django system checks"

check-deploy:
	$(call manage,check --deploy)

help-check-deploy:
	@echo "check-deploy — Production readiness checks"

shell-plus:
	$(call manage,shell_plus)

help-shell-plus:
	@echo "shell-plus — Django shell_plus"

show-urls:
	$(call manage,show_urls)

help-show-urls:
	@echo "show-urls — List URL patterns"

diffsettings:
	$(call manage,diffsettings)

help-diffsettings:
	@echo "diffsettings — Show settings differences"

test:
	$(call manage,test $(ARGS))

help-test:
	@echo "test — Run Django tests (ARGS=app)"

# ============================================================
# WAGTAIL
# ============================================================

wagtail-init:
	$(MAKE) migrate ENV=$(ENV)
	$(MAKE) collectstatic ENV=$(ENV)
	$(call manage,setup_pages)

help-wagtail-init:
	@echo "wagtail-init — Bootstrap Wagtail"

update-index:
	$(call manage,update_index)

help-update-index:
	@echo "update-index — Update search index"

rebuild-index:
	$(call confirm_prod,Rebuild PRODUCTION index?)
	$(call manage,update_index --rebuild)

help-rebuild-index:
	@echo "rebuild-index — Full index rebuild"

# ============================================================
# CELERY
# ============================================================

celery-active:
	$(call manage,celery inspect active)

help-celery-active:
	@echo "celery-active — Show active tasks"

celery-queues:
	$(call manage,celery inspect active_queues)

help-celery-queues:
	@echo "celery-queues — Show queues"

celery-purge:
	$(call confirm_prod,Purge Celery queues?)
	$(call manage,celery purge)

help-celery-purge:
	@echo "celery-purge — Purge all queues"

# ============================================================
# MEDIA
# ============================================================

thumbs-clear:
	$(call manage,thumbnail_cleanup)

help-thumbs-clear:
	@echo "thumbs-clear — Clear thumbnails"

thumbs-rebuild:
	$(call manage,rebuild_thumbnails)

help-thumbs-rebuild:
	@echo "thumbs-rebuild — Rebuild thumbnails"

# ============================================================
# DATA
# ============================================================

aces-import:
	$(call confirm_prod,Import ACES into PRODUCTION?)
	$(call manage,aces_import --file "$(FILE)")

help-aces-import:
	@echo "aces-import — Import ACES XML"
	@echo "Usage: make aces-import FILE=aces.xml"

pies-import:
	$(call confirm_prod,Import PIES into PRODUCTION?)
	$(call manage,pies_import --file "$(FILE)")

help-pies-import:
	@echo "pies-import — Import PIES XML"

sync-all:
	$(call confirm_prod,Run full sync in PRODUCTION?)
	$(call manage,sync_all)

help-sync-all:
	@echo "sync-all — Run all data syncs"

# ============================================================
# DATABASE
# ============================================================

BACKUP_DIR := ./_db_backups
STAMP := $(shell date +%Y%m%d_%H%M%S)

db-backup:
	mkdir -p $(BACKUP_DIR)
	$(call exec,$(DB),pg_dump -U $$DB_USER -d $$DB_NAME -Fc) > $(BACKUP_DIR)/$(ENV)_$(STAMP).dump

help-db-backup:
	@echo "db-backup — Backup database"

db-restore:
	$(call confirm_prod,Restore database in PRODUCTION?)
	cat "$(FILE)" | $(call exec,$(DB),pg_restore -U $$DB_USER -d $$DB_NAME --clean)

help-db-restore:
	@echo "db-restore — Restore database"
	@echo "Usage: make db-restore FILE=backup.dump"

db-reset:
	$(call confirm,RESET DEV database?)
	$(MAKE) down ENV=dev ARGS="-v"
	$(MAKE) up ENV=dev ARGS="-d --build"
	$(MAKE) migrate ENV=dev

help-db-reset:
	@echo "db-reset — Destroy and recreate DEV database"

# ============================================================
# FORMATTING
# ============================================================

format:
	$(call exec,$(WEB),black .)
	$(call exec,$(WEB),ruff check . --fix)

help-format:
	@echo "format — Auto-format Python (Black + Ruff)"

format-check:
	$(call exec,$(WEB),black --check .)
	$(call exec,$(WEB),ruff check .)

help-format-check:
	@echo "format-check — Check formatting only"

lint:
	$(call exec,$(WEB),ruff check .)

help-lint:
	@echo "lint — Run linters"

# ============================================================
# GIT
# ============================================================

git-status:
	git status

help-git-status:
	@echo "git-status — Git status"

git-sync:
	git fetch --all --prune
	git pull --rebase

help-git-sync:
	@echo "git-sync — Fetch and rebase"

git-clean:
	$(call confirm,Remove untracked files?)
	git clean -fd

help-git-clean:
	@echo "git-clean — Remove untracked files"

# ============================================================
# PIP
# ============================================================

pip-compile:
	pip-compile requirements/base.in \
		--output-file requirements/base.txt --upgrade
	pip-compile requirements/development.in \
		--output-file requirements/development.txt --upgrade
	pip-compile requirements/production.in \
		--output-file requirements/production.txt --upgrade

help-pip-compile:
	@echo "pip-compile — Compile pip requirements"

# ============================================================
# BUNDLES
# ============================================================

dev:
	$(MAKE) up ENV=dev ARGS="-d --build"
	$(MAKE) migrate ENV=dev

help-dev:
	@echo "dev — Bootstrap development environment"

doctor:
	$(MAKE) ps ENV=$(ENV)
	$(MAKE) check ENV=$(ENV)
	$(MAKE) diffsettings ENV=$(ENV)

help-doctor:
	@echo "doctor — Environment diagnostics"

# ============================================================
# SCHEMAS
# ============================================================

schemas:
	python -m infrastructure.schemas.tooling.generate
