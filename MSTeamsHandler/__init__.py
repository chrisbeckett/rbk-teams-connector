import pymsteams
import azure.functions as func
import dateutil.parser
import logging
import os
import requests

teams_webhook_url = os.environ['TEAMS_WEBHOOK_URL']
rsc_tenant_url = os.environ['RSC_TENANT_URL']

if not teams_webhook_url:
    logging.error(
        f'Teams webhook URL is not defined. Add this to the function environment variables')

if not rsc_tenant_url:
    logging.error(
        f'RSC tenant URL not defined. Add this to the function environment variables')

# Check the RSC URL is reachable
rsc_url_status = requests.get(rsc_tenant_url)
if rsc_url_status.status_code != 200:
    logging.info(
        f'RSC tenant URL does not seem to be responding, please check the environment variable')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        'Rubrik SaaS Microsoft Teams Connector HTTP trigger function processed a request.')
    try:
        source_message = req.get_json()
        logging.info(f'Finding alert message content is - {source_message}')
        logging.info(f'Teams Webhook URL set to: {teams_webhook_url}')
        logging.info(
            f'Rubrik Security Cloud tenant ID set to: {rsc_tenant_url} ')
        if source_message:
            alert_summary = source_message.get('summary')
            alert_severity = source_message.get('severity')
            alert_timestamp = source_message.get('timestamp')
            alert_class = source_message.get('class')
            alert_event_id = source_message['custom_details']['seriesId']
            alert_object_name = source_message['custom_details']['objectName']
            alert_object_type = source_message['custom_details']['objectType']
            alert_cluster_id = source_message['custom_details']['clusterId']
            alert_formatted_timestamp = dateutil.parser.parse(alert_timestamp)
            alert_display_timestamp = alert_formatted_timestamp.ctime()
            review_findings_url = rsc_tenant_url + "/events"

            logging.info(f'Building Teams message card...')
            teams_message = pymsteams.connectorcard(teams_webhook_url)
            teams_message.text("Rubrik has reported a new " +
                               alert_severity + " severity " + alert_class + " event")
            teams_message.title("Rubrik - Event Notification")
            teams_message.addLinkButton(
                "Review latest events", review_findings_url)
            teams_message.color("ff7474")
            teams_message_section = pymsteams.cardsection()
            teams_message_section.activityImage(
                "https://rgteamshandler8a2f.blob.core.windows.net/images/Rubrik_Logo.png")
            teams_message_section.title("Alert Information")
            teams_message_section.addFact("Summary: ", alert_summary)
            teams_message_section.addFact("Severity: ", alert_severity)
            teams_message_section.addFact("Type: ", alert_class)
            teams_message_section.addFact("Event ID: ", alert_event_id)
            teams_message_section.addFact("Object Name: ", alert_object_name)
            teams_message_section.addFact(
                "Object Type: ", alert_object_type)
            teams_message_section.addFact("Cluster ID: ", alert_cluster_id)
            teams_message_section.addFact("Time: ", alert_display_timestamp)
            teams_message.addSection(teams_message_section)
            logging.info(f'Sending Teams message card...')
            teams_message.send()
            msg = "Operation complete - Teams message successful"
            logging.info(f'{msg}')
            return func.HttpResponse(status_code=200)

    except Exception as e:
        logging.info(f'Bad request. {e}')
        return func.HttpResponse(status_code=400)
