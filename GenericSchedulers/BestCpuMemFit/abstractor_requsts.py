import requests
import os
import logging

ABSTRACTOR_URL = os.environ.get("RESOURCE_ABSTRACTOR_URL", "localhost")
ABSTRACTOR_PORT = int(os.environ.get("RESOURCE_ABSTRACTOR_PORT", "-1"))
API = "/api/resources?job_id="


def get_available_resources(job_id):
    available_resources = []
    if ABSTRACTOR_PORT > 0:
        try:
            URL = ABSTRACTOR_URL + ":" + str(ABSTRACTOR_PORT) + API + str(job_id)
            logging.debug("Resource request to: " + URL)
            response = requests.get(URL, timeout=5)
            logging.debug("Resource response: " + str(response))
            if response.status_code == 200:
                available_resources = response.json().get('resources', [])
        except Exception as e:
            logging.error(e)

    return available_resources
