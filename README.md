# Дипломный проект по профессии «Fullstack-разработчик на Python»

## Облачное хранилище My Cloud

### Серверная часть приложения (бэкенд) должна соответствовать следующим требованиям:

1. Реализация на Python с использованием фреймворка Django и СУБД Postgres для хранения информации.

2. Настройки приложения, такие как параметры подключения к БД, размещения файлового хранилища и т. п., выделены в коде в отдельный модуль.

3. Загрузка статических ресурсов (HTML, CSS, JS-файлы фронтенда), а также API-вызовы обрабатываются единым сервером.

4. В проекте созданы все миграции, необходимые для инициализации БД в работоспособное состояние, — создание БД, таблиц, пользователя admin с правами администратора.

5. Все API-вызовы соответствуют семантическим правилам для REST API, для обмена данными между фронтендом и бэкендом используется формат JSON.

6. Сервер содержит реализацию бэкенда для двух основных блоков приложения: административный интерфейс и работа с файловым хранилищем.

7. Административный интерфейс включает следующие функции (конкретные API-вызовы вам необходимо спроектировать самостоятельно):

- [x] регистрация пользователя — с валидацией входных данных на соответствие требованиям, описанным выше;
- [x] получение списка пользователей;
- [x] удаление пользователя;
- [x] аутентификация пользователя;
- [x] выход пользователя из системы — logout.

Общие комментарии к этому блоку:

- данные о пользователях должны храниться в таблице(ах) БД в полях, имеющих соответствующие им типы: логин, полное имя, email, пароль, признак администратора, путь к хранилищу пользователя относительно общего пути к хранилищу файлов;
- все вызовы, кроме регистрации пользователя, требуется защитить проверкой аутентификации пользователя в системе;
- функция удаления пользователей должна быть доступна только пользователю, имеющему признак администратора;
- ошибки должны возвращаться из API в виде соответствующих статус-кодов, а также в формате JSON.

8. Блок работы с файловым хранилищем содержит следующие функции (конкретные API-вызовы вам необходимо спроектировать самостоятельно):

- получение списка файлов пользователя;
- загрузка файла в хранилище;
- удаление файла из хранилища;
- переименование файла;
- изменение комментария к файлу;
- скачивание файла;
- формирование специальной ссылки на файл для использования внешними пользователями;
- скачивание файла через специальную ссылку, используемую внешними пользователями или веб-приложениями.

Общие комментарии к этому блоку:

- все функции работы с хранилищем должны проверять права доступа пользователя к хранилищу;
- необходимо, чтобы администратору была доступна работа с хранилищем любого пользователя — функция получения списка файлов должна принимать параметр с указанием хранилища, если пользователь — администратор; 
- файлы должны сохраняться на диске сервера под уникальными именами в системе папок, не допускающей конфликтов имён в случае, если разные пользователи загружают файлы с одинаковыми именами;
- для каждого файла в БД должна сохраняться следующая информация: оригинальное имя файла, размер, дата загрузки, последняя дата скачивания, комментарий, путь к файлу в хранилище, специальная ссылка, по которой файл может быть скачан внешним пользователем;
- необходимо, чтобы базовая папка для хранения файлов настраивалась как параметр системы;
- специальная ссылка на файлы должна формироваться в максимально обезличенном виде, т.е. не содержать в себе имени пользователя, информации о его хранилище и оригинальном имени файла;
- необходимо, чтобы при скачивании файла по такой ссылке он выгружался сервером с указанием оригинального имени.

Общие требования к серверу:

- состояние аутентификации пользователя должно отслеживаться через сохранение информации о сессии;
- все API-вызовы должны проверять права доступа пользователя и возвращать соответствующие ошибки через HTTP-статус и сообщение в формате JSON;
- все события сервера должны логироваться путём вывода на консоль сообщений «debug», «info», «warning», «error» с указанием даты и времени, содержать информацию, достаточную для анализа работоспособности и отладки сервера.

*Примечание*

Для лучшего понимания задачи рекомендуем ознакомиться с функционалом существующих аналогичных проектов, например Google Drive, Яндекс Диск, Dropbox и т. п. Поскольку время, отводимое на работу над проектом, ограничено, предполагается реализация только основных функций в упрощённом варианте.

------

### Правила сдачи работы

1. Опубликуйте все изменения в файлах проекта в публичном(ых) репозитории(ях) на github.com. Убедитесь, что репозитории содержат действительно последние версии со всеми изменениями.
2. Попробуйте самостоятельно с нуля развернуть приложение, следуя инструкции, описанной вами в README.md. Убедитесь, что приложение разворачивается успешно, что оно работоспособно, протестируйте основные функции.
3. Приложите в личном кабинете ссылки на репозиторий(ии) и развёрнутое приложение или укажите, что приложение может быть развёрнуто вами в течение 1 рабочего дня по запросу проверяющего.
4. Отправьте дипломную работу на проверку.
5. В случае возвращения проекта на доработку и устранения замечаний выполните необходимые действия в короткий срок и повторно сдайте работу. Если потребуется что-то уточнить и задать какие-либо вопросы по результатам проверки, свяжитесь с руководителем вашего дипломного проекта.

------

### Критерии оценки

1. Результаты работы должны быть сданы в виде ссылок на публичный(е) репозиторий(и) с кодом на github.com, а также на развёрнутое приложение на reg.ru.

2. В корневой папке репозиториев должны обязательно содержаться файлы README.md с детальным описанием структуры папок и файлов проекта, а также инструкции по его развёртыванию и запуску, достаточно подробные для выполнения специалистом, прошедшим профессиональное обучение.

3. В случае применения дополнительных инструментов, которые не изучались в программе, должны быть приложены ссылки на документацию по их установке и использованию.

4. Если код фронтенда и бэкенда опубликован в раздельных репозиториях, общие инструкции по развёртыванию приложения должны быть описаны в README.MD в репозитории с бэкендом, а в репозитории с фронтендом должны быть инструкции по сборке и подготовке артефактов фронтенда, необходимых для развёртывания.

5. Для минимизации затрат на использование ресурсов платформы reg.ru в период проверки работ допускается развёртывание приложения на reg.ru в момент, согласованный с руководителем диплома, при условии, что такое развёртывание было заранее отработано и не занимает продолжительное время.

6. В сданной работе должен быть полностью реализован соответствующий требованиям функционал из разделов, помеченных как обязательные, и может быть частично или полностью реализован дополнительный функционал.

7. Поскольку профессия fullstack-разработчика предполагает владение всеми технологиями, используемыми при разработке комплексных приложений с пользовательским интерфейсом, оценке подлежит также внешний вид приложения и удобство пользования им. Недостатки, которые ведут к существенным трудностям в работе пользователя с приложением, могут быть основанием для отправки проекта на доработку и устранения замечаний. При этом дипломный руководитель будет исходить из того, что оцениваемое приложение не является коммерческим продуктом для конечного пользователя, его использование предполагается опытными ИТ-специалистами. Рекомендуется, чтобы все элементы интерфейса приложения, которые могут вызвать сложности у такого пользователя, были снабжены явными или всплывающими подсказками, а также описаны в README.md.

8. При проверке развёрнутое приложение должно быть работоспособным в объёме реализованного обязательного функционала.

9. Развёртывание приложения должно повторно осуществляться не его разработчиком по инструкциям, содержащимся в README.md, без использования каких-либо инструментов или зависимостей, не описанных в README.md. Результатом такого развёртывания должно стать работоспособное приложение, реализующее обязательный функционал.