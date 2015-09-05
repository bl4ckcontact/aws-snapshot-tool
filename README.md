# AWS Snapshot Tool

AWS snapshotting in one command.
**This is a work in progress. Use at your own risk!**

## Configuration

This tool utilizes the *boto* library, and as such, requires the same configuration schema. To learn how to properly create your configuration file, [http://boto.readthedocs.org/en/latest/boto_config_tut.html](check out the documentation).

To get started quickly your configuration file should be named `.boto` and reside in your users home directory.
i.e. `~/.boto`

Place the following in your configuration file, replacing settings as indicated below:

```[Credentials]
aws_access_key_id = <YOUR-KEY-ID>
aws_secret_access_key = <YOUR-SECRET-KEY>

[Boto]
ec2_region_name = <YOUR-REGION-NAME>
ec2_region_endpoint = <YOUR-REGION-ENDPOINT>
```
