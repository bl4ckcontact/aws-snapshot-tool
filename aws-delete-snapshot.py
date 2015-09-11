#!/usr/bin/env python
import argparse
import os
import datetime
import boto.ec2
from botohelper import BotoHelper
from prettytable import PrettyTable

bh = BotoHelper(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'))
conn = boto.ec2.EC2Connection()

parser = argparse.ArgumentParser(description='Delete your private snapshots in your AWS region')
parser.add_argument('-n', '--dry-run', action='store_true', dest='dry_run', default=False,
                    help="Perform a dry run")
parser.add_argument('-d', '--days', dest='days', nargs=1, type=int,
                    help="Retain 'x' days of snapshots", required=True)
parser.add_argument('-w', '--weeks', dest='weeks', nargs=1, type=int,
                    help="Retain 'x' weeks of snapshots", required=True)
args = parser.parse_args()
print(args.dry_run)


def main():
    # Define PrettyTable columns
    pt = PrettyTable(['Source Volume', 'Created', 'Snapshot Description', 'Status'])
    # Slide it on over to the left
    pt.align['Instance Name'] = "l"
    pt.padding_width = 1
    # Connect to AWS with the keys in ~/.boto
    snapshots = conn.get_all_snapshots(owner="self")
    for snapshot in snapshots:
        current_time = datetime.datetime.now()
        start_time = datetime.datetime.strptime(snapshot.start_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        if start_time < current_time - datetime.timedelta(weeks=args.weeks[0], days=args.days[0]):
            try:
                del_snap = conn.delete_snapshot(snapshot, dry_run=args.dry_run)
            except boto.exception.EC2ResponseError, ex:
                    if ex.status == 403:
                        del_snap = ex.reason.upper() + ": " + "Access denied."
                    else:
                        del_snap = 'ERROR: ' + ex.error_message
            finally:
                del_snap = str(del_snap)
            pt.add_row([snapshot.volume_id, snapshot.start_time, snapshot.description, del_snap])
    print pt

if __name__ == '__main__':
    main()
