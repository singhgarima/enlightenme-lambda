import os
from base64 import b64decode

import boto3
from click.testing import CliRunner
from enlightenme import enlightenme

try:
    from interesting_email import InterestingEmail
except ImportError:
    from .interesting_email import InterestingEmail

DEFAULT_KEYWORDS = ['python', 'golang', 'chaos engineering',
                    'chaostoolkit', 'CNCF', 'cloud', 'kubernetes',
                    'docker']


def lambda_handler(event=None, context=None):
    print("Event: ", event)
    print("Context: ", context)

    result = run_enlighten_command_and_get_news()
    if result.exit_code == 0:
        send_email(OUTPUT_CSV_FILE)

    print("OUTPUT: ", result.output)


def run_enlighten_command_and_get_news():
    command = ['source', 'hacker-news',
               '--format', 'csv',
               '--output', OUTPUT_CSV_FILE,
               '--keywords', KEYWORDS
               ]
    print('run command ', command)
    result = CliRunner().invoke(enlightenme.cli, command)
    print('result ', result)
    return result


def send_email(output_file_name: str) -> None:
    email = InterestingEmail(TO_EMAIL_ADDRESSES, FROM_EMAIL_ADDRESS)
    email.create(output_file_name)
    email.send(username=SES_USERNAME, password=SES_PASSWORD)


def decrypt_encrypted_environment_variables(env_var_key: str) -> str:
    encrypted_value = os.environ[env_var_key]
    return boto3.client('kms').decrypt(CiphertextBlob=b64decode(encrypted_value))['Plaintext'].decode("utf-8")


IS_AWS_LAMBDA_ENV = True if "LAMBDA_TASK_ROOT" in os.environ else False
FROM_EMAIL_ADDRESS = os.environ.get('FROM_EMAIL_ADDRESS')
TO_EMAIL_ADDRESSES = os.environ.get('TO_EMAIL_ADDRESSES').split(",")
OUTPUT_CSV_FILE = os.path.join("/tmp", 'news.csv')
KEYWORDS = os.environ.get("KEYWORDS", ",".join(DEFAULT_KEYWORDS))
if IS_AWS_LAMBDA_ENV:
    SES_USERNAME = decrypt_encrypted_environment_variables('SES_USERNAME')
    SES_PASSWORD = decrypt_encrypted_environment_variables('SES_PASSWORD')
else:
    SES_USERNAME = os.environ.get('SES_USERNAME')
    SES_PASSWORD = os.environ.get('SES_PASSWORD')
