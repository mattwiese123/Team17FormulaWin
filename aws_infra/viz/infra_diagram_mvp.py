from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.aws.compute import EC2
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.vcs import Github
from diagrams.custom import Custom
from diagrams.aws.network import Route53


with Diagram("FormulaWin AWS Infrastructure", show=False, direction="LR"):
    users = Users("FormulaWin users")
    with Cluster("AWS", direction="LR"):
        dns = Route53("FormulaWin.com")
        with Cluster("Webapp"):
            ec2_web = EC2("Webapp Server")
            with Cluster("Webapp Containers"):
                nginx = Nginx("reverse proxy")
                dash = Custom("dashboard", "./plotly_logo_dark.png")

        db = Postgresql("RDS")

        with Cluster("Pipelines"):
            ec2_data = EC2("Pipeline/Model Server")

    with Cluster("Code Base", direction="LR"):
        gh = Github("")
        # with Cluster("Code Base"):
        #     with Cluster("Web App"):
        #         web_app_group = [
        #             Custom("IaC", "./opentofu.png"),
        #             Python("Dash code"),
        #             Docker("Docker configs"),
        #         ]
        #     with Cluster("Data"):
        #         data_code_group = [Python("Model code"), Python("ETL code")]

    dns >> ec2_web
    ec2_web >> db

    db << ec2_data

    gh - ec2_web
    gh - ec2_data

    users >> dns
