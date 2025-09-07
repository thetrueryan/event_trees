# Event Tree Architect 🌳

## Описание  
**Event Tree Architect** — это редактор для построения и управления древовидными цепочками событий.  
Каждое событие наследуется от предыдущего, образуя гибкую структуру сценариев.  
Данный редактор позволяет динамически управлять цепочками событий, динамически менять, удалять и обновлять события.
События могут иметь три статуса-маркера: **past**, **current**, **future** — для наглядной аналитики.  

### Примеры применения  
- 📈 Планирование торговых стратегий  
- 🎬 Построение сюжетов и сценариев  
- 🗂 Организация повседневных задач  

---

## Возможности ✨
- Создание и редактирование деревьев событий (CRUD API)  
- Удаление событий без нарушения структуры дерева  
- Разбиение дерева на несколько веток  
- Гибкая работа со статусами событий  
- Поддержка нескольких независимых деревьев  

---

## Технологии ⚙️
- **Язык программирования**: Python 3.12
- **Backend**: FastAPI, SQLAlchemy 2.0, Pydantic, Alembic
- **JWT и хеширование**: PyJWT, Bcrypt
- **База данных**: PostgreSQL
- **Кеширование**: Redis
- **Контейнеризация**: Docker, docker-compose  
- **Разработка и деплой**: Gitlab CI CD

---

## ![Пример древа событий](images/diagrama.png)

 ---
 
## Установка 🚀
1. Клонируем репозиторий
```bash
git clone git@github.com:thetrueryan/event_trees.git
cd event_trees
```
2. Генерация ключей
```bash
mkdir jwt_keys # создаем папку с ключами
cd jwt_keys
openssl genrsa -out jwt-private.pem 2048 # Генерируем приватный ключ
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem # Генерируем публичный ключ
```   
3. Установка и запуск через Poetry (рекомандуется)
```bash
pip install poetry # если не установлен
poetry install # установка зависимостей
poetry shell
uvicorn src.main:app --reload
```
4. Через pip
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```
5. Через docker
Важно!!! При запуске через docker необходимо дополнительно добавить JWT ключи в .env для генерации .pem файлов с ними в контейнере.
```bash
JWT_PUBLIC_KEY="YOUR_KEY" # добавить в .env публичный ключ
JWT_PRIVATE_KEY="YOUR_KEY" # добавить в .env приватный ключ
```
запускаем через docker compose
```bash
docker-compose up --build -d
```



