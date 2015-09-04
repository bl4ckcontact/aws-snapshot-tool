#!/usr/bin/env python
import os
import datetime
import logging
from botohelper import BotoHelper
from prettytable import PrettyTable

logger = logging.getLogger(__name__)


def main():
    logger.log = logging.basicConfig(filename="test.log",
                                     level=logging.INFO,
                                     format='%(asctime)s.%(msecs)d %(levelname)s: %(message)s',
                                     datefmt="%Y-%m-%d %H:%M:%S")
    logger.info("Connecting to Amazon EC2")
    bh = BotoHelper(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'))
    volumes = bh.get_all_volumes()

    # Backup all the instances!
    print("\nInitiating snapshots of all instances located in region: " + bh.ec2.region.name)

    # PrettyTable Columns
    pt = PrettyTable(['Instance Name', 'Volume', 'Snapshot Description', 'Status'])
    pt.align['Instance Name'] = "l"
    pt.padding_width = 1

    for v in volumes:

        if v.attach_data.instance_id is not None:

            instance_name = bh.get_instance_name(v.attach_data.instance_id)
            vol_name = v.__dict__['tags']['Name']
            snapshot_prefix = str(datetime.date.today()) + "_"
            snapshot_description = snapshot_prefix.replace(" ", "_") + vol_name.replace(" ", "_")

            try:
                logger.info("Attempting to snapshot '%s' on instance '%s'" % (vol_name, instance_name))
                backup_result = bh.backup_instance(instance_name, snapshot_prefix)
            except Exception, ex:
                if ex.status == 403:
                    backup_result = ex.reason.upper() + ": " + "Access denied."
                    logger.error(backup_result)
                else:
                    backup_result = 'ERROR: ' + ex.__dict__ + ex.error_message
            finally:
                backup_result = str(backup_result)

            pt.add_row([instance_name, vol_name, snapshot_description, backup_result])

    print pt

if __name__ == '__main__':
    main()
