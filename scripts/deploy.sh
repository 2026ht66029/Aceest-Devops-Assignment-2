#!/usr/bin/env bash
set -euo pipefail

STRATEGY="${1:-rolling}"
VERSION="${2:-3.2.4}"
IMAGE_REPOSITORY="${3:-YOUR_DOCKERHUB_USER/aceest-fitness}"
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

case "$STRATEGY" in
  rolling|blue-green|canary|shadow|ab-testing) ;;
  *) echo "Usage: $0 {rolling|blue-green|canary|shadow|ab-testing} [version] [image-repository]" >&2; exit 2 ;;
esac

IMAGE="${IMAGE_REPOSITORY}:${VERSION}"
kubectl apply -f "$ROOT_DIR/k8s/namespace.yaml"
sed "s|IMAGE_PLACEHOLDER|${IMAGE}|g" "$ROOT_DIR/k8s/${STRATEGY}.yaml" | kubectl apply -f -

case "$STRATEGY" in
  rolling) kubectl rollout status deployment/aceest-rolling -n aceest --timeout=180s ;;
  blue-green)
    kubectl rollout status deployment/aceest-blue -n aceest --timeout=180s
    kubectl rollout status deployment/aceest-green -n aceest --timeout=180s
    echo "Blue and green are ready. Switch traffic with: kubectl patch service aceest-blue-green -n aceest -p '{\"spec\":{\"selector\":{\"app\":\"aceest\",\"track\":\"green\"}}}'"
    ;;
  canary) kubectl rollout status deployment/aceest-canary -n aceest --timeout=180s ;;
  shadow) kubectl rollout status deployment/aceest-shadow -n aceest --timeout=180s ;;
  ab-testing)
    kubectl rollout status deployment/aceest-variant-a -n aceest --timeout=180s
    kubectl rollout status deployment/aceest-variant-b -n aceest --timeout=180s
    ;;
esac

kubectl get pods,svc -n aceest -o wide
