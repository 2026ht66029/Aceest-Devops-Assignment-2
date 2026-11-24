#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${1:-aceest}"
BASE_PORT="${BASE_PORT:-18080}"

echo "=== Blue-green selector transition ==="
echo -n "before="
kubectl -n "$NAMESPACE" get service aceest-blue-green -o jsonpath='{.spec.selector.track}'
echo
kubectl -n "$NAMESPACE" patch service aceest-blue-green -p '{"spec":{"selector":{"app":"aceest","track":"green"}}}'
echo -n "switched="
kubectl -n "$NAMESPACE" get service aceest-blue-green -o jsonpath='{.spec.selector.track}'
echo
kubectl -n "$NAMESPACE" get endpoints aceest-blue-green -o wide
kubectl -n "$NAMESPACE" patch service aceest-blue-green -p '{"spec":{"selector":{"app":"aceest","track":"blue"}}}'
echo -n "restored="
kubectl -n "$NAMESPACE" get service aceest-blue-green -o jsonpath='{.spec.selector.track}'
echo

echo "=== Canary endpoint pool ==="
kubectl -n "$NAMESPACE" get deployment aceest-stable aceest-canary
kubectl -n "$NAMESPACE" get endpoints aceest-stable aceest-canary -o wide

echo "=== Shadow mirrored request ==="
kubectl -n "$NAMESPACE" port-forward service/aceest-stable "$BASE_PORT":80 >/tmp/aceest-stable-pf.log 2>&1 &
stable_pid=$!
kubectl -n "$NAMESPACE" port-forward service/aceest-shadow "$((BASE_PORT + 1))":80 >/tmp/aceest-shadow-pf.log 2>&1 &
shadow_pid=$!
trap 'kill "$stable_pid" "$shadow_pid" 2>/dev/null || true' EXIT
sleep 2
curl -fsS "http://127.0.0.1:${BASE_PORT}/health"
echo
curl -fsS "http://127.0.0.1:$((BASE_PORT + 1))/health"
echo

echo "=== A/B variant routes ==="
kubectl -n "$NAMESPACE" port-forward service/aceest-variant-a "$((BASE_PORT + 2))":80 >/tmp/aceest-a-pf.log 2>&1 &
variant_a_pid=$!
kubectl -n "$NAMESPACE" port-forward service/aceest-variant-b "$((BASE_PORT + 3))":80 >/tmp/aceest-b-pf.log 2>&1 &
variant_b_pid=$!
trap 'kill "$stable_pid" "$shadow_pid" "$variant_a_pid" "$variant_b_pid" 2>/dev/null || true' EXIT
sleep 2
echo "variant-a:"
curl -fsS "http://127.0.0.1:$((BASE_PORT + 2))/api/version"
echo
echo "variant-b:"
curl -fsS "http://127.0.0.1:$((BASE_PORT + 3))/api/version"
echo
