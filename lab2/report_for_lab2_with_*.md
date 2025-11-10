# Отчёт по лабораторной работе №2 со звёздочкой
Первые 2 пункта задания со звёздочкой уже есть в отчёте для лабораторной №2. В ходе выполнения работы без звёздочки написан плохой Dockerfile, 
уже содержащий более трёх плохих практик (lab2/bad_practice/Dockerfile) и хороший Dockerfile, в котором эти плохие практики исправлены с пояснением о том, почему эти практики 
применять не стоит (lab2/nice_practice/Dockerfile)/

В этом отчёте хочу описать третий пункт, необходимый для работы со звёздочкой.

## Цель
1. В хорошем файле настроить сервисы так, чтобы контейнеры в рамках этого compose-проекта так же поднимались вместе, но не "видели" друг друга по сети. 
2. Понять и объяснить принцип работы такой изоляции.

## Выполнение работы

В директорию nice_practice, в которой уже содержится исправленный докер файл и правильный .yml файл, я добавил файл separate_docker_composer_for_lab_with_*.yml.
Этот файл выполняет задание по поднятию контейнеров вместе, но при этом так, чтобы они не видели друг друга по сети. 

__Вот так выглядит этот файл__ 
```
services:
  web:
    build: .
    ports:
      - "80:80"
    volumes:
      - ./admin_secret.txt:/run/secrets/admin_secret.txt:ro
    environment:
      - ADMIN_SECRET_PATH=/run/secrets/admin_secret.txt
    restart: unless-stopped
    networks:
      - web_net
    healthcheck:
      test: ["CMD", "python", "-c", "import os,sys; sys.exit(0 if os.path.exists(os.environ.get('ADMIN_SECRET_PATH','')) else 1)"]
      interval: 10s
      timeout: 5s
      retries: 5

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: appdb
      POSTGRES_PASSWORD: postgres_password_example
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "1234:1234"
    restart: unless-stopped
    networks:
      - db_net

volumes:
  pgdata:

networks:
  web_net:
    driver: bridge
  db_net:
    driver: bridge
```

## Разберёмся почему это работает 

__Что вообще значит не видят друг друга по сети?__
```
Когда контейнеры работают в одной сети, Docker предоставляет:
- виртуальный сетевой интерфейс для каждого контейнера
- мостовую сеть для связи контейнеров
- встроенный DNS, который разрешает имена сервисов в IP-адреса контейнеров
- маршрутизацию между контейнерами в этой сети
```
Я создал сети web_net и db_net. Сервис web подключён только к web_net, а db только к db_net. Никакой общей сети между ними нет. Это значит, что встроенный Docker DNS не сможет разрешить имена сервисов друг друга, а их контейнеры не будут иметь прямого сетевого пути друг к другу.


