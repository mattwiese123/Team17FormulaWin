from diagrams import Diagram, Cluster
from diagrams.aws.compute import  LambdaFunction
from diagrams.onprem.client import Users
from diagrams.aws.compute import ElasticContainerService
from diagrams.aws.compute import EC2ContainerRegistry
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.vcs import Github
from diagrams.custom import Custom
from diagrams.programming.language import Python
from diagrams.aws.network import Route53

# code goes to Github
# from GitHub, ECR gets updated with container build
# ECS deploys webapp from ECR
# Containers are nginx as reverse proxy to python webapp connected to RDS
# Model pipeline updates to RDS

with Diagram("Clustered Web Services", show=False, direction="TB"):
    users = Users("FormulaWin users")
    with Cluster("AWS"):
        dns = Route53("FormulaWin.com")
        
        with Cluster("Webapp Containers"):
            nginx = Nginx("reverse proxy")
            ecs = ElasticContainerService("Dash webapp")

        db = Postgresql("RDS")

        with Cluster("Data Pipeline"):
            data_pipeline = LambdaFunction("data pipeline")

        ecr = EC2ContainerRegistry("ECR") 


    with Cluster("Repo"):
        gh = Github("Code")
        repo_group = [Custom("IaC", "./opentofu.png"),
                      Python("Dash code"),
                      Docker("Docker configs")]

    dns >> nginx 
    nginx >> ecs
    ecs >> db
    data_pipeline >> db

    ecr >> nginx
    ecr >> ecs
    gh >> ecr
    
    repo_group >> gh
    users >> dns
