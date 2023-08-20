from aws_cdk import (
    CfnOutput,
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_autoscaling as asg,
    aws_elasticloadbalancingv2 as elb,
    aws_iam as iam,
    Duration
)
from constructs import Construct

class CdkDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, 'cdk-demo-vpc',
            cidr = '172.20.0.0/16',
            max_azs = 2,
            enable_dns_hostnames = True,
            enable_dns_support = True, 
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name = 'Public-',
                    subnet_type = ec2.SubnetType.PUBLIC,
                    cidr_mask = 24
                ),
                ec2.SubnetConfiguration(
                    name = 'Private-',
                    subnet_type = ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask = 24
                )
            ]
        )

        alb = elb.ApplicationLoadBalancer(
            self,
            "alb",
            vpc=self.vpc,
            internet_facing=True
        )

        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80),
            "Acceso desde Internet al ALB"
        )

        listener = alb.add_listener(
            "listener80",
            port=80,
            open=True
        )

        with open("./userdata.sh") as fichero:
            userdata = fichero.read()

        ec2role = iam.Role(
            self,
            "SSMEC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            description="Rol para conectar instancias EC2 a AWS SSM"
        )

        ec2role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("policy/AmazonSSMManagedInstanceCore"))

        group = asg.AutoScalingGroup(
                self,
                "ASG",
                vpc=self.vpc,
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE4_GRAVITON,ec2.InstanceSize.MICRO),
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
                machine_image=ec2.MachineImage.from_ssm_parameter('/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-arm64-gp2'),
                min_capacity=2,
                desired_capacity=4,
                max_capacity=6,
                user_data=ec2.UserData.custom(userdata),
                role=ec2role,
                health_check=asg.HealthCheck.elb(grace=Duration.minutes(3))
        )

        group.connections.allow_from(
            alb,
            ec2.Port.tcp(80),
            "Acceso al ASG desde el ALB por puerto 80"
        )

        listener.add_targets(
            "TargetGroup",
            port=80,
            targets=[group]
        )

        CfnOutput(
            self,
            "Output",
            value=alb.load_balancer_dns_name
        )
