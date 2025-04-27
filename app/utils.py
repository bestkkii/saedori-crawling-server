import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_slack_alert(message: str):
    payload = {
        "text": message
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        # raise Exception(f"Slack 알림 실패: {response.status_code}, {response.text}")
        print(f"Slack 알림 발송: {response.status_code}, {response.text}")