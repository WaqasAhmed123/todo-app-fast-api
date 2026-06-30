# AWS Deployment Guide for FastAPI Todo App

This guide explains how to containerize your FastAPI app and deploy it to AWS using ECR and ECS.

## 1. Prepare Your App for Docker

### Files created/updated
- `Dockerfile` — container definition
- `requirements.txt` — includes `pyodbc` for SQL Server

### Dockerfile behavior
- Uses `python:3.14.6-slim`
- Installs MSSQL ODBC driver and build tools
- Installs dependencies from `requirements.txt`
- Copies app sources into `/app`
- Exposes port `8000`
- Starts `uvicorn app.main:app`

## 2. Build and test the Docker image locally

1. Build the image:
   ```powershell
   cd d:\AI\todo-app
   docker build -t todo-app:latest .
   ```

2. Run it locally:
   ```powershell
   docker run --rm -p 8000:8000 todo-app:latest
   ```

3. Open in browser:
   ```text
   http://127.0.0.1:8000/docs
   ```

> If your app needs SQL Server access from a container, either run SQL Server on a network-accessible host or use Docker networking to connect to your database.

## 3. Create an AWS ECR repository

1. Install AWS CLI and configure credentials:
   ```powershell
   aws configure
   ```
2. Create ECR repo:
   ```powershell
   aws ecr create-repository --repository-name todo-app --region us-east-1
   ```
3. Note the repository URI from the output, e.g.:
   ```text
   123456789012.dkr.ecr.us-east-1.amazonaws.com/todo-app
   ```

## 4. Push Docker image to ECR

1. Authenticate Docker to ECR:
   ```powershell
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
   ```

2. Tag the image:
   ```powershell
   docker tag todo-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/todo-app:latest
   ```

3. Push it:
   ```powershell
   docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/todo-app:latest
   ```

## 5. Deploy to AWS ECS with Fargate

### 5.1 Create an IAM role for ECS tasks
- In AWS Console, go to IAM > Roles
- Create role for `Elastic Container Service Task`
- Attach policy `AmazonECSTaskExecutionRolePolicy`

### 5.2 Create a log group (optional but recommended)

1. Open CloudWatch Logs
2. Create log group `/ecs/todo-app`

### 5.3 Create an ECS cluster

1. Go to Amazon ECS > Clusters > Create Cluster
2. Choose `Networking only` (Fargate)
3. Set cluster name: `todo-app-cluster`
4. Create cluster

### 5.4 Create a task definition

1. Open ECS > Task Definitions > Create new Task Definition
2. Choose `Fargate`
3. Task definition name: `todo-app-task`
4. Task role: none (or custom if needed)
5. Task execution role: `ecsTaskExecutionRole`
6. Add container:
   - Container name: `todo-app`
   - Image: `123456789012.dkr.ecr.us-east-1.amazonaws.com/todo-app:latest`
   - Port mappings: `8000`
   - Environment variables:
     - `DATABASE_URL`
     - `SECRET_KEY`
     - `JWT_ALGORITHM`
     - `ACCESS_TOKEN_EXPIRE_MINUTES`
   - Logging: `awslogs`, log group `/ecs/todo-app`, region `us-east-1`
7. Set memory: `512` MiB, CPU: `256` or `512`
8. Create task definition

### 5.5 Create a service

1. Go to ECS > Clusters > `todo-app-cluster`
2. Create service
3. Launch type: `FARGATE`
4. Service name: `todo-app-service`
5. Number of tasks: `1`
6. VPC and subnets: choose private/public subnets
7. Security group: allow inbound `8000` if you want direct access
8. Review and create

## 6. Expose the service with Application Load Balancer (recommended)

### 6.1 Create a load balancer
1. Open EC2 > Load Balancers > Create Load Balancer
2. Choose `Application Load Balancer`
3. Scheme: `internet-facing`
4. Listeners: HTTP `80`
5. Availability zones: select at least two

### 6.2 Create target group
1. Target type: `ip`
2. Protocol: HTTP, port `8000`
3. Health check path: `/docs` or `/openapi.json`

### 6.3 Attach service to load balancer
1. In ECS service creation, set up load balancer integration
2. Choose ALB, target group created above
3. Container name: `todo-app`
4. Container port: `8000`

### 6.4 Update security group
- ALB SG: allow inbound HTTP `80`
- ECS tasks SG: allow inbound `8000` from ALB SG only

## 7. Validate deployment

1. Open the ALB DNS name in browser
2. Confirm `http://<alb-dns>/docs` loads API documentation
3. Check ECS task status is `RUNNING`
4. Confirm CloudWatch logs are being written

## 8. Additional learning notes

### SQL Server connectivity from ECS
- If SQL Server is on your laptop, use a public IP or VPN.
- For AWS-hosted DB, use **RDS SQL Server** or **EC2 Windows with SQL Server**.
- In production, use private networking and security groups.

### Environment configuration
- Use AWS Secrets Manager or SSM Parameter Store for `SECRET_KEY` and DB credentials
- In ECS Task Definition, add secrets from Secrets Manager instead of plain env vars

### Improvements for production
- Use HTTPS with ACM certificate
- Use ECS Service Auto Scaling
- Use RDS for managed SQL Server
- Store secrets in Secrets Manager
- Use CloudWatch container logs

## 9. Example `docker build` + `docker push` commands

```powershell
cd d:\AI\todo-app

docker build -t todo-app:latest .

docker tag todo-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/todo-app:latest

docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/todo-app:latest
```

## 10. Helpful AWS CLI commands

```powershell
# List ECR repos
aws ecr describe-repositories --region us-east-1

# List ECS clusters
aws ecs list-clusters --region us-east-1

# Describe service status
aws ecs describe-services --cluster todo-app-cluster --services todo-app-service --region us-east-1
```

---

## 11. Alternative Deployment: Manual EC2 + Docker + AWS RDS SQL Server

This section covers the direct deployment flow using a single EC2 instance (`t2.micro` or `t3.micro`) running Docker, connected to a managed **AWS RDS SQL Server** instance (Express Edition). This architecture is fully covered by the AWS Free Tier.

### 11.1 Step 1: Create the AWS RDS SQL Server Database
1. Go to the **RDS Console** in AWS.
2. Click **Create Database** and configure the settings:
   * **Engine type:** Microsoft SQL Server
   * **Edition:** Express Edition (Free Tier eligible)
   * **Templates:** Free Tier (automatically selects `db.t3.micro` or `db.t2.micro`)
   * **DB instance identifier:** `todo-app-python`
   * **Master username:** `admin` (or another admin username)
   * **Master password:** Set a strong password (e.g., `todo-app-fastapi`)
   * **Storage:** 20 GB General Purpose SSD (gp2)
   * **Connectivity:** Choose **Single-AZ** (Multi-AZ is not free)
3. Under **Additional Configuration**, you can specify an initial database name if prompted (otherwise, it will default to the system database `master`).
4. Note the database **Endpoint** once created (e.g., `todo-app-python.cnmusg6eabhu.eu-north-1.rds.amazonaws.com`).

### 11.2 Step 2: Configure AWS Security Groups
By default, the RDS database blocks external traffic. You must authorize connections from your EC2 instance:
1. In the RDS Console, click on your database instance -> **Connectivity & security**.
2. Click the link under **Security groups** (this opens the Security Group panel).
3. Click the **Inbound rules** tab -> **Edit inbound rules**.
4. Add a new rule:
   * **Type:** `MS SQL` (Port 1433)
   * **Source:** Select the Security Group of your EC2 instance (or `Anywhere-IPv4` / `0.0.0.0/0` temporarily for testing).
5. Save the rules.

### 11.3 Step 3: Run SQL Server locally in Docker (Optional / Dev testing)
If you choose to run SQL Server locally inside the EC2 instance instead of RDS, keep in mind that SQL Server has a hard-coded check requiring at least **2 GB of RAM** to start. Since `t2.micro`/`t3.micro` only has 1 GB of RAM, it will crash. 

To run it on a 1 GB instance, you must configure **Swap Space** on the EC2 host:
```bash
# Allocate a 1.5 GB swap file
sudo fallocate -l 1.5G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Create the docker network and run SQL Server
sudo docker network create todo-network
sudo docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=YourPassword123!" \
  --name sqlserver --network todo-network -v mssql-data:/var/opt/mssql -d mcr.microsoft.com/mssql/server:2022-latest
```

### 11.4 Step 4: Create the Database on RDS
AWS RDS restricts administrative users from creating tables inside the default `master` database. You must create a dedicated application database (e.g. `todo_app_python`) before running the FastAPI container:

Run this one-off Docker command in your EC2 terminal (replacing `YOUR_PASSWORD` and endpoint):
```bash
sudo docker run -it --rm waqasahmed07/todo-app-fast-api python -c "import pyodbc; conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=todo-app-python.cnmusg6eabhu.eu-north-1.rds.amazonaws.com,1433;DATABASE=master;UID=admin;PWD=YOUR_PASSWORD;Encrypt=yes;TrustServerCertificate=yes', autocommit=True); conn.cursor().execute('CREATE DATABASE todo_app_python'); print('Database created successfully')"
```

### 11.5 Step 5: Start the FastAPI App Container on EC2
Run the web application container on EC2, injecting the environment variables (replacing `<YOUR_PASSWORD>` and your database host):

```bash
sudo docker run -d -p 80:8000 --name todo-app \
  -e DATABASE_URL='mssql+pyodbc://admin:<YOUR_PASSWORD>@<db_url>/todo_app_python?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes' \
  -e SECRET_KEY='your_secret_key_here' \
  -e JWT_ALGORITHM='HS256' \
  -e ACCESS_TOKEN_EXPIRE_MINUTES='30' \
  waqasahmed07/todo-app-fast-api
```

Check the logs using `sudo docker logs todo-app` to verify it successfully starts and runs Uvicorn on port 8000. You can then access the documentation page at `http://<YOUR-EC2-PUBLIC-IP>/docs`.