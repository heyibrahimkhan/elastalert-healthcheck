# ElastAlert-HealthCheck


### Description:
* **What it is**: A simple script that can be executed periodically to know the status of ElastAlert execution via the latest values in *<writeback_index>*\_status.
* **Sample Commands**: 
  * python script.py -h
  * python script.py -eu X.X.X.X -ep X -ei X -swh X


### Usage:
```
usage: script.py [-h] [-eu <elasticsearch_url>] [-ep <elasticsearch_port>] [-ei <elasticsearch_index>]
                 [-swh <slack_web_hook>] [-hp <heatlhcheck_period>]

optional arguments:
  -h, --help            show this help message and exit
  -eu <elasticsearch_url>, --elasticsearch_url <elasticsearch_url>
                        ElasticSearch URL/IP. Eg: "test.elk.com"...
  -ep <elasticsearch_port>, --elasticsearch_port <elasticsearch_port>
                        ElasticSearch Port. Eg: 80
  -ei <elasticsearch_index>, --elasticsearch_index <elasticsearch_index>
                        ElasticSearch index / index pattern to read elastalert healthcheck statistics from. Eg:
                        elastalert_index, elastalert_index*
  -swh <slack_web_hook>, --slack_web_hook <slack_web_hook>
                        Slack webhook goes in it. Eg: https://hook.....
  -hp <heatlhcheck_period>, --heatlhcheck_period <heatlhcheck_period>
                        Health check period. Eg: "now-30m"
```


### How-Tos:
* **Crontab**: Setup the script as a crontab to execute periodically.