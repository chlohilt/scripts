import boto3
from datetime import datetime, timezone, timedelta


def get_all_lambdas():
    client = boto3.client('lambda', region_name='us-west-2')
    paginator = client.get_paginator('list_functions')
    lambda_functions = []

    for page in paginator.paginate():
        lambda_functions.extend(page['Functions'])

    return lambda_functions


def get_last_invoked(function_name):
    client = boto3.client('logs', region_name='us-west-2')
    log_group_name = f'/aws/lambda/{function_name}'

    try:
        streams = client.describe_log_streams(logGroupName=log_group_name, orderBy='LastEventTime', descending=True)
        if streams['logStreams']:
            last_event_timestamp = streams['logStreams'][0]['lastEventTimestamp']
            last_invoked_time = datetime.fromtimestamp(last_event_timestamp / 1000, timezone.utc)
            return last_invoked_time
        else:
            return None
    except client.exceptions.ResourceNotFoundException:
        return None


def main():
    with open("monitoringLambdasInfo.txt", "w") as file:
        for function in get_all_lambdas():
            function_name = function['FunctionName']
            one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)

            if 'prd' in function_name:
                last_invoked_time = get_last_invoked(function_name)
                if last_invoked_time:
                    if last_invoked_time < one_year_ago:
                        file.write(f"Function: {function_name}, Last Invoked: {last_invoked_time}, Invoked last OVER "
                                   f"A YEAR ago\n")
                    else:
                        file.write(f"Function: {function_name}, Last Invoked: {last_invoked_time}\n")
                else:
                    file.write(f"Function: {function_name}, Last Invoked: NEVER\n")

    file.close()


if __name__ == "__main__":
    main()
    f = open("monitoringLambdasInfo.txt", "r")
    print(f.read())
