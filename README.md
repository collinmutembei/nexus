# Nexus Products API Service

## Overview
Nexus is a Django-based API service for managing products, orders, and customers, supporting authentication via Keycloak OIDC and PostgreSQL as the database backend.

---

## Prerequisites
- Python 3.12+
- PostgreSQL
- Keycloak (OIDC Provider)
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- Docker & Minikube (for local Kubernetes deployment)

---

## Local Development Setup

### 1. Clone the Repository
```bash
gh repo clone collinmutembei/nexus
cd nexus
```

### 2. Install Dependencies
```bash
uv pip install --system --no-cache-dir -r pyproject.toml
```

### 3. Set Up Environment Variables
Create a `.env` file or export the following variables in your shell:
```bash
export SECRET_KEY=your-django-secret-key
export POSTGRES_DB=nexus
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=yourpassword
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export OIDC_CLIENT_ID=nexus-client
export OIDC_CLIENT_SECRET=your-client-secret
export OIDC_PROVIDER_DISCOVERY_URI=http://localhost:8080/realms/master/.well-known/openid-configuration
export DEFAULT_FROM_EMAIL=webmaster@localhost
export ADMIN_EMAIL=admin@localhost
export AFRICASTALKING_USERNAME=your_at_username
export AFRICASTALKING_API_KEY=your_at_api_key
```

### 4. Prepare the Database
```bash
python manage.py migrate
python manage.py createcachetable
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

---

## Keycloak OIDC Configuration

1. **Create a Realm and Client**
   - In Keycloak admin, create a new realm (or use `master`).
   - Create a new client (e.g., `nexus-client`) with `openid-connect` protocol.
   - Set `Access Type` to `confidential` and enable `Service Accounts` if needed.
   - Set valid redirect URIs (e.g., `http://localhost:8000/auth/sso-callback`).

2. **Add Custom Attribute `phone_number`**
   - Go to the client, select `Client Scopes` > `Mappers` > `Create`.
   - Name: `phone_number`, Mapper Type: `User Attribute`, User Attribute: `phone_number`, Token Claim Name: `phone_number`, Add to ID token and access token: ON.
   - Ensure users have a `phone_number` attribute set in their profile.

3. **Get Client ID and Secret**
   - In the client settings, copy the `Client ID` and `Secret` for use in your environment variables.

---

## Environment Variables Reference
| Variable                  | Description                        |
|---------------------------|------------------------------------|
| SECRET_KEY                | Django secret key                  |
| POSTGRES_DB               | Postgres database name             |
| POSTGRES_USER             | Postgres user                      |
| POSTGRES_PASSWORD         | Postgres password                  |
| POSTGRES_HOST             | Postgres host                      |
| POSTGRES_PORT             | Postgres port                      |
| OIDC_CLIENT_ID            | Keycloak OIDC client ID            |
| OIDC_CLIENT_SECRET        | Keycloak OIDC client secret        |
| OIDC_PROVIDER_DISCOVERY_URI| Keycloak OIDC discovery URI        |
| DEFAULT_FROM_EMAIL        | Default sender email               |
| ADMIN_EMAIL               | Admin notification email           |
| AFRICASTALKING_USERNAME   | Africa's Talking username          |
| AFRICASTALKING_API_KEY    | Africa's Talking API key           |

---

## Running in Minikube (Kubernetes)

### 1. Start Minikube
```bash
minikube start
```

### 2. Deploy PostgreSQL and Keycloak
- Use Helm charts or manifests to deploy PostgreSQL and Keycloak in your Minikube cluster.
- Example (using Helm):
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgres bitnami/postgresql --set auth.postgresPassword=yourpassword,auth.database=nexus
helm install keycloak bitnami/keycloak --set auth.adminPassword=admin
```

### 3. Build and Deploy Nexus Service
- Build Docker image:
```bash
eval $(minikube docker-env)
docker build -t nexus:latest .
```
- Create Kubernetes manifests for the Nexus deployment and service (example below):

<details>
<summary>Example Deployment YAML</summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nexus
  template:
    metadata:
      labels:
        app: nexus
    spec:
      containers:
      - name: nexus
        image: nexus:latest
        env:
        - name: SECRET_KEY
          value: "your-django-secret-key"
        # ...other env vars as above
        ports:
        - containerPort: 8000
```
</details>

- Apply your manifests:
```bash
kubectl apply -f k8s/
```

### 4. Connect Services
- Ensure your Nexus deployment uses the correct service names for Postgres and Keycloak (e.g., `postgres` and `keycloak` as hosts).
- Update environment variables in your deployment accordingly.

### 5. Access the Service
- Expose the Nexus service via NodePort or Ingress.
- Example:
```bash
kubectl port-forward svc/nexus 8000:8000
```
- Access at [http://localhost:8000](http://localhost:8000)

---

## Notes
- Ensure Keycloak users have the `phone_number` attribute set for proper integration.
- For production, update security settings and use persistent storage for Postgres and Keycloak.

---

## License
MIT
