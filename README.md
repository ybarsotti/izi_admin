#IZI - ADMIN - V1

###Primeira execução

Para iniciar o projeto, use o docker-compose:

```shell script
docker-compose up -d --build
```

###Executar o setup


Copie o arquivo .env.example para a pasta `izi_admin/config` como `.env`
```shell script
docker-compose exec py bash

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver 0:8000 
```

Iniciar o celery
```shell script
celery -A uwaken_admin worker -l info
```