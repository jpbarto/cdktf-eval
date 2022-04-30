#!/usr/bin/env python
from constructs import Construct
from cdktf import (
    App,
    NamedRemoteWorkspace,
    TerraformStack,
    TerraformOutput,
    RemoteBackend,
)
from cdktf_cdktf_provider_aws import AwsProvider, ec2


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, "AWS", region="us-west-1")

        instance = ec2.Instance(
            self,
            "compute",
            ami="ami-01456a894f71116f2",
            instance_type="t2.micro",
            tags={"Name": "CDKTF-eval", "Dept": "Finance", "Creator": "jpbarto"},
        )

        TerraformOutput(
            self,
            "public_ip",
            value=instance.public_ip,
        )


app = App()
stack = MyStack(app, "cdktf-eval")

RemoteBackend(
    stack,
    hostname="app.terraform.io",
    organization="jasbarto-tlz",
    workspaces=NamedRemoteWorkspace("cdktf-eval-m3"),
)

app.synth()
