from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.aws.compute import EC2
from diagrams.onprem.database import Postgresql
from diagrams.onprem.vcs import Github
from diagrams.custom import Custom
from diagrams.aws.network import Route53


with Diagram("FormulaWin IaC Pipeline", show=False, direction="LR"):
    user = User("FormulaWin Dev")
    with Cluster("AWS", direction="LR"):
        dns = Route53("FormulaWin.com")
        with Cluster("Webapp"):
            ec2_web = EC2("Webapp Server")

        db = Postgresql("RDS")

        with Cluster("Pipelines"):
            ec2_data = EC2("Pipeline/Model Server")

    with Cluster("Code Base", direction="LR"):
        gh = Github("")

    tofu = Custom("IaC", "./opentofu.png")

    gh >> user >> tofu
    tofu >> [dns, ec2_web, ec2_data, db]
