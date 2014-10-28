# Документация

Демо котел.

# 1 Управление пользователем
Подписка, разовая оплата? демодоступ?
уровни доступа

# 2 Сбор данных и (возможно управление)
Продумать объем данных, срок хранения и кол-во тагов.
Синхронизация
просмотр сырых данных

Откуда извлекать?
MySQL(возможность указания схемы) MsSQL, csv, OPC, api, apps(написать библиотеку для С).
MicDaemon

Сравнить программы логирования.
fluentd
logstash
rsyslog
collectd
scribe
nxlog


# 3 Аналитика и представление
d3.js
Подумать о структуре

# 4 События и предупреждения
смс сервисы


# Планирование
https://freedcamp.com/micont_fXP/micdata_OAU/todos

# Технологии
elasticsearch
HTTPS, REST/HATEOAS, JSON
http://www.hypercat.io/

http://graphite.readthedocs.org/en/latest/overview.html
http://graphite-api.readthedocs.org/en/latest/

# полезно взять
www.datadoghq.com

http://grafana.org/

#читать timeseries db's
http://1248.io/
http://druid.io/docs/0.6.152/
http://influxdb.com/

#остальное
Mysql proxy

http://dieter.plaetinck.be/on-graphite-whisper-and-influxdb.html

https://github.com/graphite-ng/carbon-relay-ng
http://influxdb.com/
http://dieter.plaetinck.be/monitorama-pdx-metrics20.html

https://github.com/Dieterbe/graphite-api-influxdb-docker
http://metrics20.org/implementations/
http://likens.us/deploying-influxdb-to-replace-graphite.html

https://www.dataloop.io/
https://ru.wikipedia.org/wiki/Nagios
https://github.com/vimeo/graph-explorer

https://www.serverdensity.com/
http://www.serverdensity.com/comingsoon/


https://gist.github.com/otoolep/4ebdae64412f7b3dc06b     скрипт графана нгинкс инлакс

http://dweet.io/


# localization
http://l20n.org/learn/
https://github.com/eligrey/l10n.js


# d3 mydashboard
http://krispo.github.io/angular-nvd3/#/quickstart

#dashboards
https://github.com/DataTorrent/malhar-angular-dashboard
https://github.com/nickholub/angular-dashboard-app
https://github.com/sdorra/angular-dashboard-framework

#notifications
https://slack.com/
https://www.hipchat.com/pricing
http://www.pagerduty.com/
webhooks


#beginning
django for reg
dashboard form influx_admin
UserDB(Model):
    host
    port
    name
    ds_users[]
    api_key

Dashboards(Model):
    json_struct

/settings/
    user dbs
    create db(with user)
    no more than 5


#Русские решения
http://web-telemetry.ru/

#Цены
демо 7дней бесплатно
10GB 
калькулятор размера

#grabber
nx-log easiest + windows

http://www.treasuredata.com/
tempodb

# electricity bills
http://www.meters.taipit.ru/electro/catalog/25/
http://etrivia.ru/goods/Datchik-temperatury-ds18b20


# IoT
https://xively.com/?from_cosm=true
https://xively.com/solution/by_opportunity/
