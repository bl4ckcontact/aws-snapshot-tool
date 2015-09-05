#!/usr/bin/env python
import os
import datetime
import logging
import boto.ec2
from botohelper import BotoHelper
from prettytable import PrettyTable

logger = logging.getLogger(__name__)


def main():
    logger.log = logging.basicConfig(filename="test.log",
                                     level=logging.INFO,
                                     format='%(asctime)s %(levelname)s: %(message)s',
                                     datefmt="%Y-%m-%d %H:%M:%S")
    logger.info("***** Connecting to Amazon EC2 *****")
    bh = BotoHelper(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'))
    volumes = bh.get_all_volumes()
    print("\nInitiating snapshots of all instances located in region: " + bh.ec2.region.name)
    # Define PrettyTable columns
    pt = PrettyTable(['Instance Name', 'Volume', 'Snapshot Description', 'Status'])
    pt.align['Instance Name'] = "l"
    pt.padding_width = 1

    # For every volume that is attached to an instance and has a tag 'Snapshot' = 'true' , back it up
    for v in volumes:
        # check if volume is attached to an instance
        if v.attach_data.instance_id is not None:
            # fetch instance name
            instance_name = bh.get_instance_name(v.attach_data.instance_id)
            vol_name = v.tags['Name']
            snapshot_prefix = str(datetime.date.today()) + "_"
            snapshot_description = snapshot_prefix.replace(" ", "_") + vol_name.replace(" ", "_")
            # if 'Snapshot' tag exists on volume and equals 'true', back it up
            if v.tags.get('Snapshot') == 'true':
                # try to back up volume. if it fails, log it and return the exception
                try:
                    logger.info("Attempting to snapshot '%s' on instance '%s'" % (vol_name, instance_name))
                    backup_result = bh.backup_instance(instance_name, snapshot_prefix)
                except boto.exception.EC2ResponseError, ex:
                    if ex.status == 403:
                        backup_result = ex.reason.upper() + ": " + "Access denied."
                    else:
                        backup_result = 'ERROR: ' + ex.error_message
                finally:
                    backup_result = str(backup_result)
                # add the table rows with volumes and their respective data
                pt.add_row([instance_name, vol_name, snapshot_description, backup_result])
    # show me the money!
    print pt

if __name__ == '__main__':
    main()
