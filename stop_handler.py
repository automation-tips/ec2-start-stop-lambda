# -*- coding: utf-8 -*-
from __future__ import print_function
import boto3

# インスタンスがあるリージョンを指定
REGION_NAME = 'ap-northeast-1'
# インスタンスの状態をリストで指定
# STATE_LIST = ['running','stopped']
# STATE_LIST = ['stopped']
STATE_LIST = ['running']
# インスタンスにつけているタグの名前をリストで指定
TAG_LIST = ['Environment','Dev']

def get_instance_list(ec2):
    """
    タグとステータスを指定してインスタンスを取得
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
    """
    instances = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': STATE_LIST},
            {'Name': 'tag-key', 'Values': TAG_LIST}
        ]
    )['Reservations']

    instance_list = []

    for instance in instances:
        instance_list.append(instance['Instances'][0]['InstanceId'])

    return instance_list

def stop_instances(ec2, instance_list):
    response = ec2.stop_instances(InstanceIds=instance_list)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', REGION_NAME)

    instance_list = get_instance_list(ec2)
    if len(instance_list) == 0:
      return 0

    stop_instances(ec2, instance_list)
    return 0

# 手元で起動する時にたたくやーつ
# lambda_handler("hoge", "huga")
