# Backend

## Миграции БД (Alembic)

В этом шаблоне **структура БД управляется миграциями Alembic**, а не через `create_all` при старте приложения.

- **Применить миграции**:

```bash
docker compose exec backend alembic upgrade head
```

- **Создать миграцию (автогенерация из моделей SQLAlchemy)**:

```bash
docker compose exec backend alembic revision -m "your_message" --autogenerate
```

## Бэкап / дамп PostgreSQL (docker-compose)

- **Дамп в файл на хосте**:

```bash
docker compose exec -T postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > backup.sql
```

- **Восстановление из дампа**:

```bash
cat backup.sql | docker compose exec -T postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

## MySQL (если позже решите перейти)

Alembic остаётся тем же. Обычно меняются:
- `DATABASE_URI` (схема подключения)
- зависимости-драйверы (например, вместо `asyncpg` → `aiomysql`/`asyncmy`)
