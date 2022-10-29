## Todo

#### Run the app:
```
docker-compose up -d
```
#### Create db:
```

echo "CREATE DATABASE tododb;" | psql -U user -h localhost -p 5432  # password=pass

```
#### Apply migrations:
```
docker-compose exec web alembic upgrade head
```

API docs at http://localhost:8000/docs
