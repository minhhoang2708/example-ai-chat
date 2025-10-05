
import pulumi
from pulumi_aws import lambda_ as aws_lambda, iam

# Create IAM role for Lambda
lambda_role = iam.Role(
    "lambda-role",
    assume_role_policy=pulumi.Output.all().apply(lambda _: '{"Version": "2012-10-17", "Statement": [{"Action": "sts:AssumeRole", "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}}]}')
)

# Attach policies to the role
lambda_policy = iam.RolePolicy(
    "lambda-policy",
    role=lambda_role.id,
    policy=pulumi.Output.all().apply(lambda _: '{"Version": "2012-10-17", "Statement": [{"Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], "Effect": "Allow", "Resource": "arn:aws:logs:*:*:*"}, {"Action": "lambda:*", "Effect": "Allow", "Resource": "*"}]}' )
)

for i in range(1, 4):
    lambda_func = aws_lambda.Function(
        f"lambda{i}",
        role=lambda_role.arn,
        runtime="python3.13",
        handler="app.handler",
        code=pulumi.AssetArchive({
            ".": pulumi.FileArchive(f"../lambdas/lambda{i}")
        })
    )
    pulumi.export(f"lambda{i}_arn", lambda_func.arn)
