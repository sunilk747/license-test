iimport daiquiri
import logging

daiquiri.setup(level=logging.DEBUG)
_logger = daiquiri.getLogger(__name__)


class PyPiEmr:
    """Class that encapsulates emr instance creation code.
    """

    def submit_pypi_job(self, client, aws_key, aws_id, environment=None):
        """Function to create a EMR instance and run the jon to retrain the ml model."""
        log_uri = 's3://ssamal-anchor-packages/logs'
        s3_bootstrap_uri = 's3://ssamal-anchor-packages/bootstrap.sh'
        response = client.run_job_flow(
            Name='sunil-test',
            LogUri=log_uri,
            ReleaseLabel='emr-5.10.0',
            Instances={
                'KeepJobFlowAliveWhenNoSteps': False,
                'TerminationProtected': False,
                'Ec2SubnetId': 'subnet-50271f16',
                'Ec2KeyName': 'Zeppelin2Spark',
                'InstanceGroups': [
                    {
                        'Name': 'sunil-test',
                        'InstanceRole': 'MASTER',
                        'InstanceType': 'm3.xlarge',
                        'InstanceCount': 1,
                        'Configurations': [
                            {
                                "Classification": "spark-env",
                                "Properties": {},
                                "Configurations": [
                                    {
                                        "Classification": "export",
                                        "Configurations": [],
                                        "Properties": {
                                            "LC_ALL": "en_US.UTF-8",
                                            "LANG": "en_US.UTF-8",
                                            "AWS_S3_ACCESS_KEY_ID": aws_key,
                                            "AWS_S3_SECRET_KEY_ID": aws_id
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ],
            },
            BootstrapActions=[
                {
                    'Name': 'Metadata setup',
                    'ScriptBootstrapAction': {
                        'Path': s3_bootstrap_uri
                    }
                }
            ],
            Steps=[
                {
                    'Name': 'clone repo',
                    'ActionOnFailure': 'TERMINATE_CLUSTER',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['wget', 'https://raw.githubusercontent.com/sunilk747/license-test/master/hello.py',
                                 '-P', '/home/hadoop/tmp']
                    }
                },
                {
                    'Name': 'Run program',
                    'ActionOnFailure': 'TERMINATE_CLUSTER',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['/bin/sh', '-c',
                                 "PYTHONPATH='/home/hadoop' python3.6"
                                 " /home/hadoop/tmp/hello.py"]
                    }
                }
            ],
            Applications=[{'Name': 'MXNet'}],
            VisibleToAllUsers=True,
            JobFlowRole='EMR_EC2_DefaultRole',
            ServiceRole='EMR_DefaultRole'
        )
        output = {}
        if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:

            output['training_job_id'] = response.get('JobFlowId')
            output['status'] = 'work_in_progress'
            output[
                'status_description'] = "The training is in progress. Please check the given " \
                                        "training job after some time."
        else:
            output['training_job_id'] = "Error"
            output['status'] = 'Error'
            output['status_description'] = "Error! The job/cluster could not be created!"
            _logger.debug(response)

        return output
