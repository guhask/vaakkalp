#!/bin/bash
# VaakKalp — One-command Google Cloud Run Deployment
# Usage: chmod +x deploy.sh && ./deploy.sh

set -e

PROJECT_ID=$(gcloud config get-value project)
REGION="asia-south1"
SERVICE="vaakkalp"
IMAGE="gcr.io/$PROJECT_ID/$SERVICE"

echo "🚀 Deploying VaakKalp to Cloud Run..."
echo "   Project : $PROJECT_ID"
echo "   Region  : $REGION"
echo ""

# Build & push container
gcloud builds submit --tag "$IMAGE" .

# Deploy to Cloud Run
gcloud run deploy "$SERVICE" \
  --image "$IMAGE" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

echo ""
echo "✅ VaakKalp deployed successfully!"
gcloud run services describe "$SERVICE" --region "$REGION" \
  --format="value(status.url)" | xargs -I{} echo "🌐 Live URL: {}"
