# Querido Diário

## Repositório para armazenamento de script de recomendação de trechos de diário oficial com base em uma determinada consulta

Saiba mais https://queridodiario.ok.org.br/

### Iniciando

## Modelo relacional

https://dbdiagram.io/d/64148a09296d97641d88d037

#### Docker Postgres

    ```bash
    docker run --name postgres-qdrec --env-file .env -p 5432:5432 -d postgres
    ```

#### Create stg database

        ```bash
        sudo docker exec -it postgres-qdrec psql -U queridodiario -c "CREATE DATABASE qdrec"
        ```

#### Create main table

        ```bash
        sudo docker exec -it postgres-qdrec psql -U queridodiario -d qdrec -c "CREATE TABLE IF NOT EXISTS excerpts_metadata (excerpt_id PRIMARY KEY, data_publicacao DATE, municipio TEXT, estado TEXT)"
        ```

#### Create table with vector column to NLP model

        ```bash
        sudo docker exec -it postgres-qdrec psql -U queridodiario -d qdrec -c "CREATE EXTENSION IF NOT EXISTS cube"
        sudo docker exec -it postgres-qdrec psql -U queridodiario -d qdrec -c "CREATE EXTENSION IF NOT EXISTS earthdistance"
        sudo docker exec -it postgres-qdrec psql -U queridodiario -d qdrec -c "CREATE TABLE IF NOT EXISTS excerpts_vectors (excerpt_id PRIMARY KEY, excerpt_vector TSVECTOR, FOREIGN KEY (excerpt_id) REFERENCES excerpts_metadata (excerpt_id))"
        ```

#### Create table for other entities

        ```bash
        sudo docker exec -it postgres-qdrec psql -U queridodiario -d qdrec -c "CREATE TABLE IF NOT EXISTS named_entity (excerpt_id NOT NULL, content VARCHAR, entity_type VARCHAR, start_offset INT, end_offset INT, FOREIGN KEY (excerpt_id) REFERENCES excerpts_metadata (excerpt_id), FOREIGN KEY (excerpt_id) REFERENCES excerpts_vectors (excerpt_id))"
        ```

#### get the query that will get a new vector and compare with vector tables bringing the 5 next

        ```bash
        sudo docker exec -it postgres-qdrec psql -U queridodiario -d qdrec -c "SELECT excerpt_id, texto_tsvector, earth_distance(ll_to_earth(-23.5505, -46.6333), ll_to_earth(-23.5505, -46.6333)) AS distance FROM excerpts_vectors ORDER BY distance LIMIT 5"
        ```
