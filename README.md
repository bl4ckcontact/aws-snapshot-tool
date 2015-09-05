# AWS Snapshot Tool

AWS snapshotting in one command.

This AWS snapshotting tool helps you simply snapshot specific volumes within a region, as specified in a configuration file. More specifically it looks for any volumes that contain a custom tag with a `'Snapshots': 'true'` key/value.

Information will be printed to stdout in a table, such at the one below:

```
+-----------------+-----------------------+------------------------------+---------------------------------------------------+
| Instance Name   |         Volume        |     Snapshot Description     |                       Status                      |
+-----------------+-----------------------+------------------------------+---------------------------------------------------+
| Instance_A      |       Volume A 1      |     2015-09-05_Volume_A_1    | SUCCESS: The snapshot was initiated successfully. |
| Instance_A      |       Volume A 2      |     2015-09-05_Volume_A_2    | SUCCESS: The snapshot was initiated successfully. |
| Instance_B      |       Volume B 1      |     2015-09-05_Volume_B_1    | SUCCESS: The snapshot was initiated successfully. |
| Instance_C      |       Volume C 1      |     2015-09-05_Volume_C_1    | SUCCESS: The snapshot was initiated successfully. |
+-----------------+-----------------------+------------------------------+---------------------------------------------------+
```

**This is a work in progress. Use at your own risk!**

## Requirements
In order to use this tool, you must have Python 2.7 installed in addition to the `boto` and `prettytable` modules, which you can install by running:

```$ pip install boto prettytable```

_Additionally, any volumes desired to be snapshotted must have the custom tag `'Snapshot'` and its value must be `'true'`. Any volumes without this tag will be ignored._

## Configuration

This tool utilizes the *boto* library, and as such, requires the same configuration schema. To learn how to properly create your configuration file, [http://boto.readthedocs.org/en/latest/boto_config_tut.html](check out the documentation).

To get started quickly your configuration file should be named `.boto` and reside in your users home directory.
i.e. `~/.boto`

Place the following in your configuration file, replacing settings as indicated below:

```
[Credentials]
aws_access_key_id = <YOUR-KEY-ID>
aws_secret_access_key = <YOUR-SECRET-KEY>

[Boto]
ec2_region_name = <YOUR-REGION-NAME>
ec2_region_endpoint = <YOUR-REGION-ENDPOINT>
```

## Run It!
```
$ python aws-snapshot.py
```
or
```
$ chmod +x aws-snapshot.py
$ ./aws-snapshot.py
```

## Logging
A log file `aws-snapshot.log` will be generated if not already present, and will append events/errors to the same.