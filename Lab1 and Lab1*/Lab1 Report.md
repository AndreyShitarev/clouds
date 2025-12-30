# Отчёт по лабораторной работе №1
## Задача
Настроить nginx по заданным требованиям
А именно:
```
1. Надо, чтобы работал по https с сертификатом
2. Принудительное перебрасывание HTTP-запросов с порта 80 на порт 443 для обеспечения безопасного соединения
3. Использовать Alias для создания псевдонимов путей к файлам или каталогам на сервере
4. Настроить виртуальные хосты для обслуживания нескольких доменных имён на одном сервере
```

## Ход работы
1. Сначала я скачал nginx-1.26.3 поменял его имя на nginx для простоты и поместил в папку для своей лаборторной

   Команда - ```Rename-Item -Path "C:\ITMO\Lab1\nginx-1.26.3" -NewName "nginx"```

2. Затем я создал 2 пет-проекта в директории html внутри nginx с именами project1 и project2 (решил сам создать проекты)

   Команда для progect1 - ```New-Item -Path "C:\ITMO\Lab1\nginx\html\project1" -ItemType Directory```
   Команда для project2 - ```New-Item -Path "C:\ITMO\Lab1\nginx\html\project2" -ItemType Directory```

3. Далее уже в папках своих проектов я создал для них простое наполнение из текста в html разметке

   Команда для progect1 - ```Set-Content -Path "C:\ITMO\Lab1\nginx\html\project1\index.html" -Value "<h1>Hello world in project1 (Windows)</h1>"```
   Команда для project2 - ```Set-Content -Path "C:\ITMO\Lab1\nginx\html\project2\index.html" -Value "<h1>Hello world in project2 (Windows)</h1>"```

4. Далее для выполнения требования по использованию Alias, я создал директорию Hidden_Storage

   Команда - ```New-Item -Path "C:\ITMO\Lab1\Hidden_Storage" -ItemType Directory```

5. Затем я наплнил только что созданную директорию текстовым файлом

   Команда - ```Set-Content -Path "C:\ITMO\Lab1\Hidden_Storage\info.txt" -Value "Secret file through Alias"```

6. Так как я работаю в Windows powershell далее я скачал win64 OpenSSL Light и созад поддиректорию ssl в конфиге nginx

   Команда - ```New-Item -Path "C:\ITMO\Lab1\nginx\conf\ssl" -ItemType Directory```

7. Потом я использовал утилтиу OpenSSL для создания самоподписывающегося сертификата, для того, чтобы сервер работал по протоколу HTTPS (с командой для этого пунка мне помог Gemini, самому разобраться не получилось)

   Команда - ```& "C:\Program Files\OpenSSL-Win64\bin\openssl.exe" req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "C:\ITMO\Lab1\nginx\conf\ssl\selfsigned.key" -out "C:\ITMO\Lab1\nginx\conf\ssl\selfsigned.crt" -subj "/C=RU/ST=Moscow/L=Moscow/O=DevOpsLab/OU=IT/CN=project1.local"```

8. Далее через блокнот я открыл nginx.config и переписал его. Прикрепляю скрин переписанного конфига (также файл лежит рядом с этим отчётом)

   
<img width="729" height="1018" alt="Screenshot 2025-12-30 151044" src="https://github.com/user-attachments/assets/15010f1d-34b1-4c94-910d-172da8386fdc" />

9. Далее мне нужно было, чтобы Windows знал, что project1.local - это мой компьюьер. Для этого я использовал следующую команду:

    Команда - ```Add-Content -Path "C:\Windows\System32\drivers\etc\hosts" -Value "`n127.0.0.1 project1.local project2.local"```

10. На этом подготовка закончилась и я запустил nginx

    Команда - ```start nginx```

11. На этапе проверки я узнал крайне забавную функцию хрома. При открытии своего проекта по ссылке https://project1.local я попал на экран-предупреждение о том, что страница не безопасна и нигде не было кнопки по типу "всё равно перейти". И оказалось, что можно кликнуть на пустую часть этой страницы и написать "thisisunsafe" (без поля ввода, нигде не отображается текст) и после того, как будет дописана последняя буква хром откроет страницу :)

- Страница ```https://project1.local```:

   <img width="1280" height="136" alt="Screenshot 2025-12-30 151943" src="https://github.com/user-attachments/assets/d23e7d9f-4cd2-4f41-abc0-2eda32585bc4" />

- Страница ```[https://project1.local](https://project2.local/docs/info.txt)```:

  <img width="1280" height="227" alt="Screenshot 2025-12-30 151947" src="https://github.com/user-attachments/assets/de3a3bbb-7a6d-4f2a-aa70-2d830952eeaf" />


  ## Итог
  Удалось насроить nginx по заданным требованиям. В процессе работы я узнал, несколько новых команд для windows powershell, понял как писать конифг для nginx, перебрасывать порты и зачем нужен alias. Ну и удивившую меня функцию Google Chrome.
