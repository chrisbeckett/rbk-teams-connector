import pymsteams
import azure.functions as func
import dateutil.parser
import logging
import json
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        'Rubrik SaaS Microsoft Teams Connector HTTP trigger function processed a request.')
    logging.info('Code version : 120522-0905 - changed alert to event')
    try:
        teams_webhook_url = 'https://chrisbeckettuk.webhook.office.com/webhookb2/6b0d9673-7820-47df-91a4-528dd8918a8a@5938e49b-e4d2-41ab-b0a0-6b9e0d6a1571/IncomingWebhook/70105b1be3504b1da50c569f9e651b9b/7029e1ea-4150-4aa6-94aa-759bf9a20c16'
        source_message = req.get_json()
        logging.info(f'Finding alert message content is - {source_message}')
        logging.info(f'Teams Webhook URL set to: {teams_webhook_url}')
        if source_message:
            #teams_webhook_url = os.getenv('TEAMS_WEBHOOK_URL')
            teams_webhook_url = 'https://chrisbeckettuk.webhook.office.com/webhookb2/6b0d9673-7820-47df-91a4-528dd8918a8a@5938e49b-e4d2-41ab-b0a0-6b9e0d6a1571/IncomingWebhook/70105b1be3504b1da50c569f9e651b9b/7029e1ea-4150-4aa6-94aa-759bf9a20c16'
            logging.info(f'Teams webhook URL set to {teams_webhook_url}')
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
            review_findings_url = "https://rxlabs.dev-016.my.rubrik-lab.com/events"

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
                "https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco,dpr_1/v1481229346/fguokibny8s46diuexkz.png")
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