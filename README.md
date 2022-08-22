# Rubrik Security Cloud Microsoft Teams Connector

## What does it do?

This connector runs as an Azure Function and provides a webhook URL for Rubrik Security Cloud (RSC, formerly Polaris) to send alerts to. This provides simple connectivity to Microsoft Teams as it sends alert information as cards into a Teams channel. The serverless function can be quickly and easily deployed using the '**Deploy to Azure**' button at the bottom of the page.

## How does it work?

Create a new webhook in the RSC "Security Settings" page (can be accessed via the gear icon in the top right hand corner) and filter out the required events and severity. For example, to send backup operations events to Teams, you may wish to select the "Backup", "Diagnostic", "Maintenance" and "System" event types with the "Critical" and "Warning" severities.

![alt text](https://github.com/chrisbeckett/rbk-teams-connector/blob/main/add-webhook.png "Rubrik webhook configuration")

![alt text](https://github.com/chrisbeckett/rbk-teams-connector/blob/main/teams-event.png "Teams screenshot")

A simple architecture diagram is shown below. In essence, we send a webhook event from RSC to an Azure Function, this then takes the raw JSON event payload and converts it into Teams "card" format and sends it to the Teams channel URL specified in the environment variable.

![alt text](https://github.com/chrisbeckett/rbk-teams-connector/blob/main/teams-connector-arch.png "Architecture overview")

## What do I need to get started?

- An RSC tenant
- A Microsoft Teams account
- A Teams channel to send alerts to
- A Teams webhook URL (https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)
- Python 3.7/3.8/3.9 (3.10 is not currently supported by Azure Functions)
- Git

## Obtaining the code

Run **git clone https://github.com/chrisbeckett/rbk-teams-connector.git**

## Deploying the Azure Function

Click the "Deploy to Azure" button and fill out the deployment form

- Both the **Azure Function** name and the **Storage Account** name **must be globally unique or deployment will fail (if a new storage account is created)**
- Once the ARM template deployment is complete, open a command prompt and navigate to the **rbk-teams-connector** folder
- Install the Azure Functions command line tools (*https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash*)
- Run **func init**
- Run **func azure functionapp publish _functname_** where the functname is your function name from the "**Deploy to Azure**" workflow
- When this is complete, you will need the HTTP trigger URL (Function overview, "Get Function URL" button)

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fchrisbeckett%2Frbk-teams-connector%2Fmain%2Fdeployment-template.json)
