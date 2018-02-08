### Assignment 1
Напишите функцию сравнения двух json-объектов.
#### Answer 1
See ```src/compare_json.py```
### Assignment 2
Есть сервер. На нём ресурс  /images , который умеет сохранять картинки, если к нему обратишься методом  POST . Необходимо написать загрузчик картинок из данной папки на данный сервис. Скрипт принимает на вход путь до папки. Запрещено пользваться волшебными функциями из бибилотек "загрузи всё сам". 
#### Answer 2
If "requests" is considered magic, and you need a more low-level upload, then something went wrong with this task. See ```src/upload_images.py```
### Assignment 3
Вы были приняты в компанию "Рога и копыта". Первым же делом Вас попросили узнать какие функции на сервере тормозят. Политика компании запрещает устанавливать дополнительные непроверенные модули, пакеты и т.д. Вам доступны стандартные функции и билиотеки. Вы можете внести свои изменения в код и загрузить код на тестовый сервер, может быть несколько раз, далее вам доступны только логи с него. Что делать?
#### Answer 3
The obvious approach is to generously sprinkle logging messages with operation description and timestamps at the beginning and the end of all user-facing methods. 
At the same time it could be useful to run strace/lsof/htop/netstat to get a sense if there's an issue with network/disk IO, or maybe even some other piece of software is hogging all of the resources and degrading server performance.
### Assignment 4
У компании "Рога и копыта" есть сервис "RED", который работает по REST и определяет количество красного цвета на изображении. Сервис стал очень популярным и компания решила добавить ещё один сервис "RED_STATS", в который "RED" скидывает сообщения о том что у такого-то клиента пришла картинка с таким-то количеством красного цвета. Для клиентов у "RED_STATS" должны появиться две следующие функции: возможность подписаться на оповещения, что пришла картинка, у которой красного больше, чем заданное клиентом значение. Получать статистику по времени, сколько вообще за данный промежуток было послано изображений, сколько изображений у которых красного было больше заданного значения. Ваша задача спроектировать работу "RED_STATS", как он будет общаться с клиентами, как хранить данные, как маштабироваться и т.д.
#### Answer 4
1. We'll use message broker to deliver events from RED to RED_STATS (Kafka/RabbitMQ/etc.). This will allow us to easily scale amount of RED_STATS instances in the future, and will have minimal performance/architecture effect on RED.
1. RED_STATS instances will subscribe to the messages from RED as a balanced group, so only a single instance of RED_STATS receives a particular message from RED.
1. RED_STATS will store RED data in a time series DB, such as Graphite, since it perfectly fits clients' needs, and since we'll have considerably more writes than reads.
1. Clients can access stats info via UI like Grafana, which will allow for highly customized data presentation. Additionally, if clients need to perform further processing of this statistical data, RED_STATS (or ideally, a new dedicated service, RED_STATS_API) can provide REST API to directly download particular stats.
1. Subscriptions can be handled either by public-facing message broker, by some kind of PubSub solution, or even by simple email notifications - it all depends on clients use of this data. If the chosen solution implies explicit subscription by clients, RED_STATS will store the clients info in a relational DB.