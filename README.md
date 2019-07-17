

# ReportDesigner


Currentiy the repo is configured for fast local debug (automatic reload). 
To readjust it back to Production:
* uncomment "web" service in `docker-compose`
* edit init_db.sql (? clarify it later)
* in `api/main.py` 
    * change link from `dev.toml` to `config.toml`
    * comment/delete next (lines 10-11)
    ```
    import aioreloader
    aioreloader.start()
    ```

```
export DB_HOST=5433
docker-compose up --build
По умолчанию создаётся одна запись в таблице
```

создать новую запись http://0.0.0.0:8080/create  
получить все записи http://0.0.0.0:8080/groups  
получить запись по id http://0.0.0.0:8080/groups/2

[Готовые данные для postman](https://www.getpostman.com/collections/a2dbeb2dc4886ddd236f) 


