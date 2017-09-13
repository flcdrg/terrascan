import unittest
import os
import terraform_validate
from . import settings


class TestAlbListener(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_alb_listener_port(self):
        # Assert that listener port is 443
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_alb_listener').property('port').should_equal('443')

    def test_alb_listener_protocol(self):
        # Assert that protocol is not http
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_alb_listener').property('protocol').should_not_equal('http')
        self.v.resources(
            'aws_alb_listener').property('protocol').should_not_equal('HTTP')

    def test_alb_listener_ssl_policy(self):
        # Assert that old ssl policies are not used
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_alb_listener').property(
            'ssl_policy').should_not_equal('ELBSecurityPolicy-2015-05')
        self.v.resources(
            'aws_alb_listener').property(
            'ssl_policy').should_not_equal('ELBSecurityPolicy-TLS-1-0-2015-04')

    def test_alb_listener_certificate(self):
        # Assert that certificate_arn is set
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_alb_listener').should_have_properties(['certificate_arn'])


class TestAMI(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_aws_ami_ebs_block_device_encryption(self):
        # Assert ami 'ebs_block_device' blocks are encrypted
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_ami').property(
            'ebs_block_device').property('encrypted').should_equal(True)

    def test_ami_ebs_block_device_kms(self):
        # Assert ami 'ebs_block_device' blocks has KMS
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_ami').property(
            'ebs_block_device').should_have_properties(['kms_key_id'])


class TestAMICopy(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_aws_ami_copy_encryption(self):
        # Assert resources are encrypted
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_ami_copy').property('encrypted').should_equal(True)

    def test_aws_ami_copy_kms(self):
        # Assert that a KMS key has been provided
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_ami_copy').should_have_properties(['kms_key_id'])


class TestAPIGatewayDomainName(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_aws_api_gateway_domain_name_certificate(self):
        # Assert that certificate settings have been configured
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_api_gateway_domain_name').should_have_properties(
            [
                'certificate_name',
                'certificate_body',
                'certificate_chain',
                'certificate_private_key'
            ])


class TestEC2Instance(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_ec2_instance_ebs_block_device_encrypted(self):
        # Assert ec2 instance 'ebs_block_device' is encrypted
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_instance').property(
            'ebs_block_device').property('encrypted').should_equal(True)


class TestCloudfrontDistribution(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_aws_cloudfront_distribution_origin_protocol_policy(self):
        # Assert that origin receives https only traffic
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_cloudfront_distribution').property(
            'origin').property(
            'custom_origin_config').property(
            'origin_protocol_policy').should_equal("https-only")

    def test_cloudfront_distro_default_cache_viewer_protocol_policy(self):
        # Assert that cache protocol doesn't allow all
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_cloudfront_distribution').property(
            'default_cache_behavior').property(
            'viewer_protocol_policy').should_not_equal("allow-all")

    def test_cloudfront_distro_cache_behavior_viewer_protocol_policy(self):
        # Assert that cache protocol doesn't allow all
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_cloudfront_distribution').property(
            'cache_behavior').property(
            'viewer_protocol_policy').should_not_equal("allow-all")


class TestCloudTrail(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_cloudtrail_kms(self):
        # Assert that a KMS key has been provided
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_cloudtrail').should_have_properties(['kms_key_id'])


class TestCodeBuild(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_cloudtrail_kms(self):
        # Assert that a KMS key has been provided
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_codebuild_project').should_have_properties(['encryption_key'])


class TestCodePipeline(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_cloudtrail_kms(self):
        # Assert that a KMS key has been provided
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_codepipeline').should_have_properties(['encryption_key'])


class TestDBInstance(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_db_instance_encrypted(self):
        # Assert that DB is encrypted
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_db_instance').property('storage_encrypted').should_equal(True)

    def test_db_instance_kms(self):
        # Assert that a KMS key has been provided
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_db_instance').should_have_properties(['kms_key_id'])


class TestDMSEndpoint(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_aws_dms_endpoint_ssl_mode(self):
        # Assert that SSL is verified
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_dms_endpoint').property(
            'ssl_mode').should_equal('verify-full')

    def test_aws_dms_endpoint_kms(self):
        # Assert that a KMS key has been provided
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_dms_endpoint').should_have_properties(
            [
                'kms_key_arn'
            ])

    def test_aws_dms_endpoint_certificate(self):
        # Assert that SSL cert has been provided
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_dms_endpoint').should_have_properties(
            [
                'certificate_arn'
            ])


class TestDMSReplicationInstance(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_aws_dms_replication_instance_kms(self):
        # Assert that a KMS key has been provided
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_dms_replication_instance').should_have_properties(
            ['kms_key_arn'])


class TestEBS(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_aws_ebs_volume_encryption(self):
        # Assert that all resources of type 'aws_ebs_volume' are encrypted
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_ebs_volume').property('encrypted').should_equal(True)

    def test_aws_ebs_volume_kms(self):
        # Assert that a KMS key has been provided
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_ebs_volume').should_have_properties(['kms_key_id'])


class TestEFSFileSystem(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_aws_ebs_volume_encryption(self):
        # Assert that all resources of type 'aws_efs_file_system' are encrypted
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_efs_file_system').property('encrypted').should_equal(True)

    def test_aws_ebs_volume_kms(self):
        # Assert that a KMS key has been provided
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_efs_file_system').should_have_properties(['kms_key_id'])


class TestElastictranscoderPipeline(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_aws_elastictranscoder_pipeline_kms(self):
        # Assert that a KMS key has been provided
        self.v.error_if_property_missing()
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_elastictranscoder_pipeline').should_have_properties(
            ['aws_kms_key_arn'])


class TestELB(unittest.TestCase):

    def setUp(self):
        # Tell the module where to find your terraform configuration folder
        self.path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), settings.TERRAFORM_LOCATION)
        self.v = terraform_validate.Validator(self.path)

    def test_aws_elb_listener_port_80(self):
        # Assert ELB listener port is not 80 (http)
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_elb').property(
            'listener').property('lb_port').should_not_equal(80)

    def test_aws_elb_listener_port_21(self):
        # Assert ELB listener port is not 21 ftp
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_elb').property(
            'listener').property('lb_port').should_not_equal(21)

    def test_aws_elb_listener_port_23(self):
        # Assert ELB listener port is not 23 telnet
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_elb').property(
            'listener').property('lb_port').should_not_equal(23)

    def test_aws_elb_listener_port_5900(self):
        # Assert ELB listener port is not 5900 VNC
        self.v.enable_variable_expansion()
        self.v.resources(
            'aws_elb').property(
            'listener').property('lb_port').should_not_equal(5900)


if __name__ == '__main__':
    unittest.main()
