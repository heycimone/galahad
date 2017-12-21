import json
import boto.ec2
import errorcodes
import time


aws_image_id = 'ami-da05a4a0' # see https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LaunchInstanceWizard:
aws_instance_type = 'm3.medium'
aws_subnet_id='subnet-0b97b651'
aws_key_name = 'valor-dev'
aws_tag_key = 'Project'
aws_tag_value = 'Virtue'

aws_state_to_virtue_state = {
	'pending': 'CREATING',
	'running': 'RUNNING',
	'shutting-down': 'DELETING',
	'terminated': 'STOPPED',
	'stopping': 'STOPPING',
	'stopped': 'STOPPED'
}

class Virtue:
	id = ''
	username = ''
	roleId = ''
	applicationIds = []
	resourceIds = []
	transducerIds = []
	state = ''
	ipAddress = ''

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
        
def get_aws_instance(virtueId):
	conn = boto.ec2.connect_to_region('us-east-1')
	for res in conn.get_all_reservations():
		for instance in res.instances:
			if instance.id == virtueId:
				return instance

	return None


def virtue_get(args):
	if 'virtueId' not in args:
		return errorcodes.get_response_error(
			errorcodes.invalidOrMissingParameters,
			'Missing argument: virtueId')

	virtueId = args['virtueId']
	instance = get_aws_instance(virtueId)
	if instance is None:
		return errorcodes.get_response_error(
			errorcodes.invalidId,
			'VirtueId not found: ' + str(virtueId))

	virtue = Virtue()
	virtue.id = instance.id
	virtue.ipAddress = instance.ip_address
	virtue.state = aws_state_to_virtue_state.get(
		instance.state, 'UNKNOWN')
	return virtue.get_json()

def virtue_create(args):
	if 'roleId' not in args:
		return errorcodes.get_response_error(
			errorcodes.invalidOrMissingParameters,
			'Missing argument: roleId')

	virtue = Virtue()
	virtue.roleId = args['roleId']

	conn = boto.ec2.connect_to_region('us-east-1')
        interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(subnet_id=aws_subnet_id,
                                                                    #groups=['sg-0365c56d'],
                                                                    associate_public_ip_address=True)
        interfaces = boto.ec2.networkinterface.NetworkInterfaceCollection(interface)
	res = conn.run_instances(aws_image_id,
		                 key_name=aws_key_name,
		                 instance_type=aws_instance_type,
                                 network_interfaces=interfaces )

	instance = res.instances[0]
	instance.add_tag(aws_tag_key, value=aws_tag_value)
	instance.add_tag('Name', value=instance.id)
	virtue.id = instance.id
        
        instance.update()
        while instance.state == "pending":
                time.sleep(1)
                instance.update()

	virtue.ipAddress = instance.ip_address
	virtue.state = aws_state_to_virtue_state.get(instance.state,
		'UNKNOWN')

	return virtue.get_json()

def virtue_launch(args):
	if 'virtueId' not in args:
		return errorcodes.get_response_error(
			errorcodes.invalidOrMissingParameters,
			'Missing argument: virtueId')

	#TODO
	return errorcodes.get_response_error(
			errorcodes.notImplemented,
			'launch not yet implemented')

def virtue_stop(args):
	if 'virtueId' not in args:
		return errorcodes.get_response_error(
			errorcodes.invalidOrMissingParameters,
			'Missing argument: virtueId')

	#TODO
	return errorcodes.get_response_error(
			errorcodes.notImplemented,
			'stop not yet implemented')

def virtue_destroy(args):
	if 'virtueId' not in args:
		return errorcodes.get_response_error(
			errorcodes.invalidOrMissingParameters,
			'Missing argument: virtueId')

	virtueId = args['virtueId']
	instance = get_aws_instance(virtueId)
	if instance is None:
		return errorcodes.get_response_error(
			errorcodes.invalidId,
			'VirtueId not found: ' + str(virtueId))

	try:
		instance.terminate()
		return errorcodes.get_response_success()
	except:
		return errorcodes.get_response_error(
			errorcodes.serverDestroyError,
			'Error destroying virtueId: ' + str(virtueId))
