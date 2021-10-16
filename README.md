# cloudphoto 

## Настройка

---

Для начала нужно перейти в папку _h_1_

Затем установить переменные среды:

    AWS_ACCESS_KEY_ID=<your_access_key_id>
    AWS_SECRET_ACCESS_KEY=<your_secret_access_key>

---

## Запуск

Команда для просмотра списка альбомов:

     python main.py list
     
Команда для просмотра списка фотографий в альбоме:

    python main.py list -a album

Команда для отправки фотографий в облачное хранилище:

    python main.py upload -p path -a album

Команда для загрузки фотографий на компьютер:

    python main.py download -p path -a album
