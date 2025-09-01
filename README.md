# Event Tree Architect 🌳

## Внимание !!
Проект находится в стадии разработки, и часть функционала еще не завершена

## Описание  
**Event Tree Architect** — это редактор для построения и управления древовидными цепочками событий.  
Каждое событие наследуется от предыдущего, образуя гибкую структуру сценариев.  
События могут иметь три статуса-маркера: **past**, **current**, **future** — для наглядной аналитики.  

### Примеры применения  
- 📈 Планирование торговых стратегий  
- 🎬 Построение сюжетов и сценариев  
- 🗂 Организация повседневных задач  

---

## Возможности ✨
- Создание и редактирование деревьев событий (CRUD API)  
- Удаление узлов без нарушения структуры дерева  
- Разбиение дерева на несколько веток  
- Гибкая работа со статусами событий  
- Поддержка нескольких независимых деревьев  

---

## Технологии ⚙️
- **Язык программирования**: Python 3.12
- **Backend**: FastAPI, SQLAlchemy 2.0, Pydantic, Alembic
- **JWT и хеширование**: PyJWT, Bcrypt
- **База данных**: PostgreSQL  
- **Контейнеризация**: Docker, docker-compose  
- **Разработка и деплой**: Gitlab CI CD

---

## Архитектура
Схема будет здесь позже \:

---

## Roadmap 📌
 - CI/CD pipeline (build & deploy stages)
 - Dockerfile и docker-compose (app + Postgres + Grafana)
 - Redis-кэширование
 - Улучшение документации
 - Демо UI (в перспективе)

 ---
 
## Установка 🚀
1. Клонируем репозиторий
```bash
git clone git@github.com:thetrueryan/event_trees.git
cd event_trees
```
2. Установка и запуск через Poetry (рекомандуется)
```bash
pip install poetry # если не установлен
poetry install # установка зависимостей
poetry shell
uvicorn src.main:app --reload
```
3. Через pip
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```
4. Через docker (в будущем)
```bash
docker-compose up --build -d 
```

