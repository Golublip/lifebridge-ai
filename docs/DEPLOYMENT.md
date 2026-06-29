# Deployment Guide - LifeBridge AI

This document provides instructions on deploying LifeBridge AI to production environments.

---

## 1. Containerized Deployment (Docker Compose)
To run both backend and frontend locally or in a cloud instance using Docker Compose:
```bash
docker-compose up --build
```
This boots:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

---

## 2. Google Cloud Run Deployment
You can deploy the backend container directly to Google Cloud Run:
```bash
gcloud builds submit --tag gcr.io/your-project-id/lifebridge-backend
gcloud run deploy lifebridge-backend --image gcr.io/your-project-id/lifebridge-backend --platform managed --allow-unauthenticated
```

---

## 3. Railway / Render Deployment
The project contains pre-configured settings:
- Copy the backend environment variable `GEMINI_API_KEY` to the deployment settings.
- Build command for frontend: `npm run build`
- Start command for frontend: `npm run start`
