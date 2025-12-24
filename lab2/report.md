# Лабораторная работа №2

## Цель

Написать 2 докер-файла
1.	Плохой (bad_practice), в котором будут допущены намеренные ошибки, файл должен быть примером того, как делать не надо и опасно.
2.	Хороший (nice_practice), в котором исправлены ошибки “плохого” докер-файла.
После написания двух файлов, проанализировать результат и сделать выводы о том, как правильно и безопасно написать докер-файл.

## Выполнение работы

Сначала я создал две директории: bad_practice – для докер-файла с ошибками, nice_practice – для исправленного. 
Давайте сравним хороший и плохой Dockerfile

### Плохой:
```

FROM debian:bookworm

RUN apt update

RUN apt install -y python3 python3-pip curl

ADD https://randomsite.com/randomarchive.tar.gz /tmp/external/

ADD . /srv/project

ENV APP_TOKEN="token_for_example"

CMD ["python3", "/srv/project/hello.py"]
```


### Хороший:
```

FROM python:3.11.4-slim

RUN addgroup --system svcgroup && adduser --system --ingroup svcgroup svcuser

WORKDIR /usr/src/app

COPY hello.py .

USER svcuser

CMD ["python", "hello.py"]
```



### Ошибки в докер фале:
1.	Cлишком общий базовый образ
•	Образ debian:bookworm - большой (100+ МБ), без предустановленного Python, он требует дополнительной установки и обновления пакетов.
•	python:3.11.4-slim - минимальный, оптимизированный для Python-приложений, безопаснее и быстрее собирается.

2.	Раздельные RUN-команды и отсутствие очистки кеша
Каждая команда RUN создаёт отдельный слой, что увеличивает размер образа.
Также кеш apt остаётся внутри слоя. В исправленном варианте всё объединено в одну команду, кеш удаляется - образ меньше и чище.

3.	Использование ADD вместо COPY
•	ADD автоматически распаковывает архивы и может скачивать файлы из интернета, что опасно.
•	COPY делает только одно. Он копирует локальные файлы. Это безопасно.

4.	Запуск под root и без WORKDIR
•	Запуск приложения от root - риск для безопасности. Если злоумышленник получит доступ, он сможет управлять всем контейнером.
•	Исправлено созданием непривилегированного пользователя и рабочей директории.

Теперь ошибки в файле docker_compose.yml

### Плохой
``` 
services:

  web:
  
    build: .
    
    privileged: true
    
    network_mode: "host"
    
    volumes:
    
      - "/:/host_root"
      
    environment:
    
      - APP_TOKEN=token_for_example
      
    ports:
    
      - "80:80"
      
  db:
  
    image: postgres:latest
    
    environment:
    
      POSTGRES_USER: postgres
      
      POSTGRES_PASSWORD: postgres_pwd
```

### Скриншот с запуском плохого Docker-файла
<img width="1280" height="324" alt="Screenshot 2025-12-24 214928" src="https://github.com/user-attachments/assets/a41e10dc-21ab-4fff-a474-c9ddb4912181" />



### Хороший
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
    
```

### Скрины запуска хорошего docker-файла
<img width="1280" height="1201" alt="Screenshot 2025-12-24 213739" src="https://github.com/user-attachments/assets/778a20d2-8d15-4136-9e11-a4da5dca686d" />
<img width="1280" height="1252" alt="Screenshot 2025-12-24 213728" src="https://github.com/user-attachments/assets/38c02ad2-d622-416b-95c0-f420fb14bf22" />

 
### Ошибки:

1.	Запуск в привилегированном режиме
Режим privileged даёт контейнеру доступ к ядру и устройствам хоста.  В исправленном варианте контейнер работает с минимальными правами.
2.	использование network_mode: host
Хорошая практика - использовать стандартную docker-сеть, чтобы контейнеры общались между собой через имя сервиса.
3.	монтирование корня файловой системы хоста
•	Монтаж / даёт контейнеру доступ ко всем файлам хоста, включая системные.
•	В исправленном варианте монтируется только один файл-секрет, причём в режиме read-only.

## Вывод

В результате выполнения этой лабораторной работы я разобрался не только в основынх ошибках при написании докер файла, но и об ошибках, которые можно допустить в yml файлах. Помимо этого, я узнал очень много новых команд Dockerfile и особенности их использования. Думаю, это полезный опыт. 
