#!/bin/sh


source ../venv/bin/activate


python manage.py get_betalists
python manage.py get_product_hunt_users
python manage.py get_product_hunts
python manage.py update_real_domains
python manage.py calc_stats
python manage.py calc_milestones