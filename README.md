# AWS Lambda MonoRepo Example

## Structure

- `lambdas/` - Contains three Python 3.13 Lambda functions
- `pulumi/` - Pulumi Python project for deployment (QA, Production stacks)
- `terraform/` - IAM roles/policies for Lambda managed via Terraform
- `.github/workflows/` - GitHub Actions CI/CD pipeline

## Lambda Functions
Each Lambda function is a simple Python handler returning "Hello World".

## Deployment
- Lambda functions and IAM roles/policies are deployed via Pulumi (`pulumi/__main__.py`).
- Pulumi stacks: `qa`, `prod`.

## CI/CD Pipeline
- **Test**: Runs for all branches/environments
- **Build**: QA and Production (Production only on `main` branch)
- **Deploy**: QA and Production (Production only on `main` branch)
- Only `main` branch can access Production build/deploy jobs

## Secrets Required
- `PULUMI_ACCESS_TOKEN`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

## Usage
1. Configure Pulumi stacks for QA and Production environments.
2. Push changes to GitHub to trigger CI/CD pipeline.
# example-ai-chat