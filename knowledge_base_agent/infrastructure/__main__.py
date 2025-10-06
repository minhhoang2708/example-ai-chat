import json
import pulumi
import pulumi_aws as aws

# Get the project and stack name for naming resources.
config = pulumi.Config()
project_name = pulumi.get_project()
stack_name = pulumi.get_stack()

# 1. Create an IAM Role for the Lambda Function
# This role grants the Lambda function permissions to run and write logs.
lambda_role = aws.iam.Role(
    f"{project_name}-lambda-role-{stack_name}",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                }
            ],
        }
    ),
    description="IAM role for the Lambda function",
)

# Attach the basic AWSLambdaVPCAccessExecutionRole policy to the role.
# This policy allows the function to write logs to CloudWatch.
aws.iam.RolePolicyAttachment(
    f"{project_name}-lambda-policy-{stack_name}",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
)

# 2. Define the Lambda Function Resource
# The code for the function is an asset that points to the zip file.
lambda_function = aws.lambda_.Function(
    f"{project_name}-lambda-{stack_name}",
    # The handler value is `filename.function_name`.
    handler="lambda_function.handler",
    runtime="python3.13",
    role=lambda_role.arn,
    code=pulumi.FileArchive("../knowledge_base_agent.zip"),
    description="A simple Python Lambda function deployed with Pulumi.",
    tags={
        "project": project_name,
        "stack": stack_name,
    },
)

# 3. Export the Lambda function's name and ARN
pulumi.export("lambda_function_name", lambda_function.name)
pulumi.export("lambda_function_arn", lambda_function.arn)
