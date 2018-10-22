from scrapy.cmdline import execute
import sys, os
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_REPO_DIR = os.path.join(BASE_DIR, "data_repo")

sys.path.append(BASE_DIR)
sys.path.append(DATA_REPO_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'data_repo.settings'
django.setup()

execute(["scrapy", "crawl", "jobbole"])