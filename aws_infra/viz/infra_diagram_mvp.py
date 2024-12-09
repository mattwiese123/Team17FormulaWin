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

    with Cluster("Code Base", direction="LR"):
        gh = Github("")

    with Cluster("Data Pipelines"):
        colab = Custom("FastF1", "./Google_Colaboratory_SVG_Logo.svg.png")

    dns >> ec2_web
    ec2_web >> db

    gh - ec2_web

    users >> dns

    db << colab
