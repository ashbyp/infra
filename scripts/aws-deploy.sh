#!/bin/bash

# === Config Variables ===
REGION="us-east-1"
REPO_NAME="my-api"
CLUSTER_NAME="my-api-cluster"
SERVICE_NAME="my-api-service"
CONTAINER_NAME="my-api"
IMAGE_TAG="latest"
CPU="256"
MEMORY="512"

# === RDS Credentials ===
DB_HOST="your-rds-endpoint.amazonaws.com"
DB_PORT="5432"
DB_USER="youruser"
DB_PASSWORD="yourpassword"
DB_NAME="yourdbname"

# === Step 1: Create ECR Repository ===
aws ecr create-repository --repository-name $REPO_NAME --region $REGION

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME"

# === Step 2: Build and Push Docker Image ===
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $REPO_URI
docker build -t $REPO_NAME .
docker tag $REPO_NAME:$IMAGE_TAG $REPO_URI:$IMAGE_TAG
docker push $REPO_URI:$IMAGE_TAG

# === Step 3: Get Default VPC and Subnet ===
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text)
SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[0].SubnetId" --output text)

# === Step 4: Create Security Group ===
SG_ID=$(aws ec2 create-security-group \
  --group-name my-api-sg \
  --description "Allow HTTP access" \
  --vpc-id $VPC_ID \
  --query "GroupId" --output text)

aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# === Step 5: Create ECS Cluster ===
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION

# === Step 6: Create Task Execution Role (only needed once) ===
aws iam create-role --role-name ecsTaskExecutionRole \
  --assume-role-policy-document file://<(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ecs-tasks.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
)

aws iam attach-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

EXEC_ROLE_ARN=$(aws iam get-role --role-name ecsTaskExecutionRole --query "Role.Arn" --output text)

# === Step 7: Register Task Definition ===
aws ecs register-task-definition --region $REGION \
  --family $CONTAINER_NAME-task \
  --network-mode awsvpc \
  --requires-compatibilities FARGATE \
  --cpu "$CPU" \
  --memory "$MEMORY" \
  --execution-role-arn $EXEC_ROLE_ARN \
  --container-definitions "[
    {
      \"name\": \"$CONTAINER_NAME\",
      \"image\": \"$REPO_URI:$IMAGE_TAG\",
      \"portMappings\": [{\"containerPort\": 80, \"protocol\": \"tcp\"}],
      \"environment\": [
        {\"name\": \"ENV\", \"value\": \"prod\"},
        {\"name\": \"DB_HOST\", \"value\": \"$DB_HOST\"},
        {\"name\": \"DB_PORT\", \"value\": \"$DB_PORT\"},
        {\"name\": \"DB_USER\", \"value\": \"$DB_USER\"},
        {\"name\": \"DB_PASSWORD\", \"value\": \"$DB_PASSWORD\"},
        {\"name\": \"DB_NAME\", \"value\": \"$DB_NAME\"}
      ]
    }
  ]"

# === Step 8: Deploy ECS Service ===
aws ecs create-service --region $REGION \
  --cluster $CLUSTER_NAME \
  --service-name $SERVICE_NAME \
  --task-definition $CONTAINER_NAME-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_ID],securityGroups=[$SG_ID],assignPublicIp=ENABLED}"
