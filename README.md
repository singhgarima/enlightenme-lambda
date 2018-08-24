# Enlightenme Lambda

## Pre-requisites

### Local Machine

Python3.6
pipenv
AWS CLI


### AWS

On the AWS side, you will need to have created:
* S3 bucket (To upload deployment package to)
* An IAM user (with access to upload to S3 and deploy/update lambda)
* A Lambda function
* A CloudWatch Scheduled event (This is optional and you can trigger it via other available triggers)

> Note: See Makefile for the name I have chosen
>       Or update names as per your AWS setup


## Setup

* AWS Lambda Source Code to run enlightenme for sending me daily updates

```bash
aws configure --profile my_profile_name
```

> Note: It is a best practice to create an IAM User and not use your
>       root account.
>       See [https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html?icmpid=docs_iam_console#create-iam-users]()

## Deploy

I have abstracted out the preparation and deployment to my Makefile:

```bash
make clean prepare deploy
```

## References:

* https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
* https://joarleymoraes.com/hassle-free-python-lambda-deployment/
* https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html?icmpid=docs_iam_console