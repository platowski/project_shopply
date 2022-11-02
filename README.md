#Quickstart on local
```
make build
make up
```

Other useful tools in Makefile

Application starts on localhost on port 8010:
```
http://localhost:8010
```


#Author's notes

I hope using DRF is not cheating. ;) I've done a quick research and it came up as a go to tool. 
I haven't put a lot of effort into auth / user part. I don't want to reinvent the wheel, so I used DRF's builtin. 

I have to admit that I like how DRF encourages to build Hypermedia/HATEOAS REST API's. 

Deployment process (imaginary)
There are two infrastructure related parts of the code:
1. circleCi config
2. AWS CDK infra as code (or Terraform/K8s )

Pipeline steps 
all branches:
- build and test (units, pytest functional, contract)
- sonarcloud quality gate inspection
- all above are requirements to unlock merge to master as well as at least 2 approvals from other devs

on master (or deploy branch):
- build image and push to ECR (container registry)
- deploy staging:
  - prepare AWS CDK change set
  - deploy change set (inject env vars from parameter store and secret manager)
  - run migrations
  - run e2e test cases
- approve prod deploy (manual step in circle)
  - prepare AWS CDK change set
  - deploy change set (inject env vars from parameter store and secret manager)
  - run migrations
  - run e2e test cases



