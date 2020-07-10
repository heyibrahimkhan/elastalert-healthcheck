import copy
import argparse
from pprint import pprint
from slack_webhook import Slack
from elasticsearch import Elasticsearch
from utils import setup_logger, set_slack_post_color, os


# global vars
#############
logger = None
slack_client = None
args = None
something_bad_happened = {
	"fallback":"ElastAlert issue...",
	"pretext":"ElastAlert issue...",
	"color": set_slack_post_color('red'),
	"fields":[
		{
			"title":"ElastAlert issue...",
			"value":"Error occurred during ElastAlert healthcheck.\nNeed to investigate manually."
		}
	]
}
# A sample attachment
# slack_message_attachment = {
# 	"fallback":"",
# 	"pretext":"",
# 	"color":"",
# 	"fields":[
# 		{
# 			"title":"Notes",
# 			"value":"This is much easier than I thought it would be."
# 		}
# 	]
# }
#####################
es_client = None
es_query = {
	'healthcheck_query': {
	  "size": 0, 
	  "query": {
	    "bool": {
	      "filter": {
	        "range": {
	          "@timestamp": {
	            "gte": "now-30m"
	          }
	        }
	      }
	    }
	  }
	}
}
#############


def setup_args():
	parser = argparse.ArgumentParser(os.path.basename(__file__))
	parser.add_argument('-eu', '--elasticsearch_url', metavar='<elasticsearch_url>', type=str, help='ElasticSearch URL/IP. Eg: test.elk.com...')
	parser.add_argument('-ep', '--elasticsearch_port', metavar='<elasticsearch_port>', type=str, help='ElasticSearch Port. Eg: 80')
	parser.add_argument('-ei', '--elasticsearch_index', metavar='<elasticsearch_index>', type=str, help='ElasticSearch index / index pattern to read elastalert healthcheck statistics from. Eg: elastalert_index, elastalert_index*')
	parser.add_argument('-swh', '--slack_web_hook', metavar='<slack_web_hook>', type=str, help='Slack webhook goes in it. Eg: https://hook.....')
	parser.add_argument('-hp', '--heatlhcheck_period', metavar='<heatlhcheck_period>', default='now-30m', type=str, help='Health check period. Eg: now-30m')
	logger.info('Successfully parsed arguments...')
	return parser.parse_args()


def initialize_g_vars():
	global logger, es_client, slack_client, args
	logger = setup_logger()
	args = setup_args()
	es_client = Elasticsearch(['{}:{}'.format(args.elasticsearch_url, args.elasticsearch_port)])
	slack_client = Slack(url=args.slack_web_hook)
	logger.info('Global variables initialized succcessfully...')


def send_slack_message(slack_client, text, slack_message_attachments=list()):
	slack_client.post(text=text, attachments=slack_message_attachments)
	logger.info('Message posted to Slack successfully...')


def get_health_check_results(es_client, es_query, elastalert_index):
	ea_is_running = False
	total_hits = None
	try:
		res = es_client.search(index=elastalert_index, body=es_query)
		if 'hits' in res and res.get('hits').get('total') > 0:
			total_hits = res.get('hits').get('total')
			ea_is_running = True
	except Exception as e:
		logger.error('Exception {} occurred in get_health_check_results()...'.format(e))
	return ea_is_running, total_hits


def update_esquery(es_query):
	es_query['query']['bool']['filter']['range']['@timestamp']['gte'] = args.heatlhcheck_period
	return es_query


def main():
	try:
		in_elbs = False
		initialize_g_vars()
		ea_is_running = False
		total_hits = None
		ea_is_running, total_hits = get_health_check_results(
			es_client,
			update_esquery(es_query.get('healthcheck_query')),
			args.elasticsearch_index
		)
		logger.info('Health check results obtained...')
		if ea_is_running:
			logger.info('ElastAlert is running...')
			logger.info('Will not send Slack message...')
		else:
			logger.info('ElastAlert is not running...')
			logger.info('Will send Slack message...')
			send_slack_message(slack_client, '', slack_message_attachments=[something_bad_happened])
		logger.info('script {} executed successfully...'.format(os.path.basename(__file__)))
	except Exception as e:
		logger.error('Exception {} occurred in main of file {}...'.format(e, os.path.basename(__file__)))
		logger.info('ElastAlert is not running...')
		logger.info('Will send Slack message...')
		send_slack_message(slack_client, '', slack_message_attachments=[something_bad_happened])


# main flow of the program
##########################
main()
##########################