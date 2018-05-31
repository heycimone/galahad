import boto3
import json

class AWS:

    def __init__(self):
        self.id = ''
        self.username = ''
        self.roleId = ''
        self.applicationIds = []
        self.resourceIds = []
        self.transducerIds = []
        self.state = ''
        self.ipAddress = ''

    def get_json(self):
        return json.dumps({'id': self.id,
            'username': self.username,
            'roleId': self.roleId,
            'applicationIds': self.applicationIds,
            'resourceIds': self.resourceIds,
            'transducerIds': self.transducerIds,
            'state': self.state,
            'ipAddress': self.ipAddress})

    def __repr__(self):
        return self.get_json()

    def __str__(self):
        return self.get_json()

    @staticmethod
    def get_id_from_ip(ip_address):
        ec2 = boto3.client('ec2')

        res = ec2.describe_instances(
            Filters=[{
                'Name': 'private-ip-address',
                'Values': [ ip_address ]
            }] )

        if( len(res['Reservations'][0]['Instances']) == 0 ):
            return None

        return res['Reservations'][0]['Instances'][0]['InstanceId']


    def instance_create(self, image_id, \
                        inst_type, \
                        subnet_id, \
                        key_name, \
                        tag_key, \
                        tag_value, \
                        sec_group, \
                        inst_profile_name, \
                        inst_profile_arn):
        """Create a new AWS instance - a virtue
        This will create a AWS instance based on a
        given AMI ID.
        Ref: http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances
        """

        ec2 = boto3.resource('ec2',region_name='us-east-1')

        res = ec2.create_instances(ImageId=image_id,
            InstanceType=inst_type,
            KeyName=key_name,
            MinCount=1,
            MaxCount=1,
            Monitoring={'Enabled':False},
            SecurityGroupIds=[sec_group],
            SubnetId=subnet_id,
            IamInstanceProfile={
                                    'Name': inst_profile_name,
                                    #'Arn': inst_profile_arn
                                },
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': tag_key,
                            'Value': tag_value
                        },
                    ]
                },
                {
                    'ResourceType': 'volume',
                    'Tags': [
                        {
                            'Key': tag_key,
                            'Value': tag_value
                        },
                    ]
                },
            ]
        )

        instance = res[0]
        self.id = instance.id

        instance.wait_until_running()
        instance.reload()

        self.ipAddress = instance.private_ip_address
        self.state = instance.state['Name']

        return instance


    def instance_launch(self, instId):
        """Start the specified AWS instance
        This will use the instance ID specifed as the AWS instance ID and start the
        instance.
        Ref: http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.start_instances
        """
        client = boto3.client('ec2')

        response = client.start_instances(
            InstanceIds=[
                instId,
            ]
        )
        return response


    def instance_stop(self, instId):
        """Stop the specified AWS instance
        Stop the specified AWS instance
        Ref: http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.stop_instances
        """
        client = boto3.client('ec2', 'us-east-1')

        # Specify the InstanceId of the spcific instance.
        response = client.stop_instances(
            InstanceIds=[
                instId,
            ]
        )
        return response


    def instance_destroy(self, instId):
        """Terminate the AWS instance
        Terminate the specified AWS instance.
        Ref: http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.terminate_instances
        """
        client = boto3.client('ec2')

        # Specify the InstanceId of the spcific instance.
        response = client.terminate_instances(
            InstanceIds=[
                instId,
            ]
        )
        return response
