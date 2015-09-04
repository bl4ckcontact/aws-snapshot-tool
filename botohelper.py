'''
Created on Jul 17, 2012
Edited by bl4ckcontact

@author: mraposa
'''
import boto


class TagError(Exception):
    pass


class BotoHelper():
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.access_key = aws_access_key_id
        self.secret_key = aws_secret_access_key
        self.ec2 = boto.connect_ec2(self.access_key, self.secret_key)
        self.s3 = boto.connect_s3(self.access_key, self.secret_key)

    def get_instance_volumes(self, instance_id):
        volumes = self.ec2.get_all_volumes(filters={'attachment.instance-id': instance_id})
        return volumes

    def get_all_volumes(self):
        volumes = self.ec2.get_all_volumes()
        return volumes

    def get_volume_attributes(self, volume_id):
        attributes = self.ec2.get_volume_attribute(volume_id)
        return attributes

    def get_instance_id(self, instance_name):
        for instance in self.get_all_instances():
            tags = instance.__dict__['tags']
            try:
                name = tags['Name']
            except KeyError:
                raise TagError("Name Tag not specified on AWS Instance: {}".format(instance))
            if instance_name.lower() == name.lower():
                return instance.id

    def get_instance_name(self, instance_id):
        for instance in self.get_all_instances():
            tags = instance.__dict__['tags']
            if instance_id == instance.id:
                try:
                    return tags['Name']
                except KeyError:
                    raise TagError("Name Tag not specified on AWS Instance: {}".format(instance))

    def get_all_instances(self):
        instances = []
        all_inst = self.ec2.get_all_instances()
        for res in all_inst:
            # each reservation have a instance:
            for instance in res.instances:
                instances.append(instance)
        return instances

    def backup_instance(self, instance_name, description_prefix="Automated_Backup"):
        volumes = self.get_instance_volumes(self.get_instance_id(instance_name))
        snapshot_description = "%s_%s" % (description_prefix, instance_name)
        for volume in volumes:
            self.ec2.create_snapshot(volume.id, snapshot_description)
            return "SUCCESS: The snapshot was initiated successfully."

    def backup_all_instances(self, description_prefix="Automated_Backup"):
        for instance in self.get_all_instances():
            tags = instance.__dict__['tags']
            try:
                name = tags['Name']
            except KeyError:
                raise TagError("Name Tag not specified on AWS Instance: {}".format(instance))
            self.backup_instance(name, description_prefix)

    def get_all_instance_status(self):
        return self.ec2.get_all_instance_status()

    def get_all_scheduled_events(self):
        """
        Get any AWS scheduled events.

        Returns a list of all the scheduled events. Each item in the list is a event dictionary
        with information about the event

        For more information see
        https://www.42lines.net/2011/12/08/listing-pending-amazon-ec2-events-using-boto-and-python/
        """
        all_events = []
        for stat in self.ec2.get_all_instance_status():
            if stat.events:
                for event in stat.events:
                    event_info = {}
                    event_info['id'] = stat.id
                    event_info['zone'] = stat.zone
                    event_info['code'] = event.code
                    event_info['description'] = event.description
                    event_info['not_before'] = event.not_before
                    event_info['not_after'] = event.not_after
                    all_events.append(event_info)
        return all_events

    def get_s3_buckets(self):
        return self.s3.get_all_buckets()

    def create_s3_bucket(self, bucket_name):  # this is the method signature
        """Create a new S3 bucket
        :param bucket_name: name of the bucket to create
        :returns: reference to a bucket object
        """
        return self.s3.create_bucket(bucket_name)
