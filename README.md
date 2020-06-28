# django-ecommerce 

### First set-up to project

```
create two folders named -> public/static and whoosh_index
```

```
execute commands to init instalation
- python manage.py migrate
- python manage.py collectstatic
- python manage.py rebuild_index
```

```
for each product registration, do the indexing with the command
- python manage.py update_index
```

