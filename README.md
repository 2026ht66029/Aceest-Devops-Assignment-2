
# ACEest Fitness and Gym DevOps Assignment 2

This package implements the Assignment 2 CI/CD pipeline for ACEest Fitness and Gym. It preserves all ten supplied application milestones, builds and validates them in version order, deliberately fails version 3.0.1 in the acceptance stage, and continues with later versions so Jenkins visibly demonstrates staged progression and rollback readiness.

The supplied milestone files are desktop Tkinter applications. They are preserved unchanged under 'versions/' and are syntax/acceptance checked without opening a GUI. The delivery layer is a container-safe Flask service derived from the ACEest fitness domain so it can run in Docker and Kubernetes with health checks, Pytest, SonarQube, and deployment strategies.

## What is included

- 'versions/': all ten supplied ACEest source versions.
- 'ci/version_manifest.json': authoritative version order and intentional failure declaration.
- 'ci/build_version.py': compiles and packages one milestone.
- 'ci/test_version.py': acceptance gate for one milestone.
- 'ci/run_version_matrix.py': local ordered matrix runner.
- 'app.py' and 'aceest/': Flask delivery application.
- 'tests/': Pytest API and manifest tests.
- 'Jenkinsfile': Jenkins pipeline with a visible stage for every version.
- 'Dockerfile': test and runtime images with version build arguments.
- 'k8s/': rolling, blue-green, canary, shadow, and A/B manifests.
- 'scripts/deploy.sh': applies a selected strategy and prints service/pod evidence.
- 'sonar-project.properties': SonarQube project configuration.
- 'report/SHORT_REPORT_TEMPLATE.md': 2–3 page report structure.
- 'evidence/SCREENSHOT_CHECKLIST.md': final screenshot checklist.

## Version order and intentional failure

| Stage | Supplied file | Result |
| --- | --- | --- |
| 1.0.0 | 'Aceestver-1.0.py' | Pass |
| 1.1.0 | 'Aceestver-1.1.py' | Pass |
| 1.1.2 | 'Aceestver1.1.2.py' | Pass |
| 2.0.1 | 'Aceestver2.0.1.py' | Pass |
| 2.1.2 | 'Aceestver-2.1.2.py' | Pass |
| 2.2.1 | 'Aceestver-2.2.1.py' | Pass |
| 2.2.4 | 'Aceestver-2.2.4.py' | Pass |
| 3.0.1 | 'Aceestver-3.0.1.py' | Intentional failed acceptance stage |
| 3.1.2 | 'Aceestver-3.1.2.py' | Pass |
| 3.2.4 | 'Aceestver-3.2.4.py' | Pass |

The source for 3.0.1 remains available and compiles. Its acceptance command returns code 2 intentionally. Jenkins wraps only this expected failure with 'catchError', marks that stage red and the overall build 'UNSTABLE', then continues to 3.1.2, 3.2.4, unit tests, Docker builds, and optional deployment. Do not hide or delete this failed stage; it is required evidence.

## 1. Prerequisites

Use a Rocky Linux 9 cloud server or the lab's equivalent Linux machine.

Minimum tools:

- Git and a public GitHub repository
- Python 3.10 or newer
- Docker Engine or Podman
- Jenkins with Pipeline, Git, JUnit, Credentials Binding, and Docker Pipeline support
- SonarQube and the SonarQube Scanner for Jenkins
- Docker Hub account
- 'kubectl' and Minikube, or a Kubernetes cluster with a LoadBalancer/Ingress solution

Recommended server capacity: 2 vCPUs, 4 GB RAM, 20 GB free disk, and access to ports 8080, 8000, 9000, and the Kubernetes service endpoint.

Never commit passwords, GitHub tokens, Docker Hub tokens, SonarQube tokens, SSH private keys, or remote-desktop URLs.

## 2. Copy the package to the server

From the computer where the ZIP is downloaded:

~~~bash
scp DevOps_Assignment_2_ACEest_MultiVersion.zip <user>@<server-ip>:~/
ssh <user>@<server-ip>
unzip DevOps_Assignment_2_ACEest_MultiVersion.zip
cd ~/DevOps_Assignment_2_ACEest_MultiVersion
chmod +x scripts/*.sh ci/*.py
~~~

If the package is already on the server, only run 'cd' and 'chmod'.

Take Screenshot 1 after extraction. Show the package directory and top-level files, but do not show tokens.

## 3. Validate every supplied version locally

~~~bash
python3 --version
python3 -m compileall -q app.py aceest ci tests
python3 ci/run_version_matrix.py --allow-expected-failure
./scripts/validate-package.sh
~~~

Expected result:

- 10 build results are printed.
- 1.0.0 through 2.2.4 pass.
- 3.0.1 prints 'TEST FAILED' and is identified as intentional.
- 3.1.2 and 3.2.4 pass.
- 'artifacts/version-matrix.json' is created.
- The validator ends with a pass message.

Take Screenshot 2 showing the full matrix and validator output.

## 4. Run the Flask tests

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --requirement requirements-dev.txt
ruff check .
pytest --cov-report=xml:coverage.xml
~~~

Expected result: Ruff passes, all Flask/manifest tests pass, and coverage is at least 90 percent.

Run the application:

~~~bash
ACEEST_VERSION=3.2.4 ACEEST_SOURCE_VERSION=3.2.4 python app.py
~~~

In another terminal:

~~~bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/version
curl http://127.0.0.1:8000/api/programs
curl -X POST http://127.0.0.1:8000/api/bmi \
  -H 'Content-Type: application/json' \
  -d '{"height_cm":180,"weight_kg":75}'
~~~

Take Screenshot 3 showing Pytest and Screenshot 4 showing '/health' and '/api/version'. Stop with Ctrl+C.

## 5. Create the GitHub repository

Create an empty public GitHub repository named 'aceest-devops-assignment-2'. Do not add another README or '.gitignore'.

~~~bash
git init
git branch -M main
git add .
git commit -m "feat: add ACEest multi-version CI CD pipeline"
git remote add origin https://github.com/<github-user>/aceest-devops-assignment-2.git
git push -u origin main
~~~

Create annotated milestone tags:

~~~bash
for version in 1.0.0 1.1.0 1.1.2 2.0.1 2.1.2 2.2.1 2.2.4 3.0.1 3.1.2 3.2.4; do
  git tag -a "app-v${version}" -m "ACEest application version ${version}"
done
git push origin --tags
~~~

Take Screenshot 5 showing the GitHub tree with 'Jenkinsfile', 'Dockerfile', 'versions', 'ci', 'tests', and 'k8s'. Take Screenshot 6 showing 'git log --oneline --decorate --all' and the tags.

## 6. Configure Jenkins

Install Jenkins using your approved Rocky Linux procedure:

~~~bash
java -version
sudo systemctl enable --now jenkins
sudo systemctl status jenkins --no-pager
~~~

Confirm these Jenkins plugins:

- Pipeline
- Git and GitHub
- JUnit
- Credentials Binding
- Docker Pipeline
- SonarQube Scanner for Jenkins
- Pipeline Utility Steps, if required by your Jenkins installation

Add credentials:

| Credential | Type | ID |
| --- | --- | --- |
| GitHub key/token | SSH key or secret text | your chosen ID |
| Docker Hub account/token | Username with password | 'dockerhub' |
| SonarQube token | Secret text | 'sonarqube-token' |

Create a Pipeline job:

1. **New Item** -> 'aceest-devops-assignment-2' -> **Pipeline**.
2. Select **Pipeline script from SCM**.
3. SCM: **Git**.
4. Repository URL: your GitHub URL.
5. Branch: '*/main'.
6. Script path: 'Jenkinsfile'.
7. Save.

Take Screenshot 7 of the job configuration with token contents hidden.

## 7. Configure SonarQube

Create a SonarQube project:

- Project key: 'aceest-fitness-multiversion'
- Project name: 'ACEest Fitness Multi Version CI CD'

Generate a token. In Jenkins, go to **Manage Jenkins -> System -> SonarQube servers**:

- Server name: 'SonarQube'
- URL: 'http://127.0.0.1:9000' when both services share the host
- Token: the configured SonarQube credential

Configure the SonarQube Jenkins webhook at 'http://<jenkins-host>:8080/sonarqube-webhook/' so the pipeline can receive the quality-gate result. The Jenkins stage waits up to five minutes and fails the build if the gate is not 'OK'.

If Jenkins and SonarQube are separate containers, use their reachable service name instead of '127.0.0.1'. Install/configure 'sonar-scanner' on the Jenkins agent. The pipeline reads 'sonar-project.properties' and 'coverage.xml'.

Take Screenshot 8 of the SonarQube project and quality gate. Do not show the token.

## 8. Run the staged Jenkins build

Run **Build with Parameters**:

- 'DOCKERHUB_REPOSITORY': '<dockerhub-user>/aceest-fitness'
- 'PUSH_DOCKER_IMAGES': false for the first run
- 'RUN_SONARQUBE': true after SonarQube is configured
- 'DEPLOY_KUBERNETES': false until the cluster is ready

Expected stages:

1. Checkout
2. Prepare Environment
3. Build 1.0.0 through Build 3.2.4
4. Validate 1.0.0 through Validate 3.2.4
5. Pytest Unit Tests
6. SonarQube Analysis
7. Docker 1.0.0 through Docker 3.2.4
8. Push Docker Hub Tags, when enabled
9. Deploy To Kubernetes, when enabled

Expected result: 'UNSTABLE', because Validate 3.0.1 is intentionally failed. Later versions must still run. Any failure in 3.1.2, 3.2.4, Pytest, Docker, or SonarQube is unexpected.

Take Screenshot 9 of Stage View showing red 'Validate 3.0.1' and green later stages. Take Screenshot 10 of console output showing the intentional failure and successful 3.1.2/3.2.4. Take Screenshot 11 of Pytest/JUnit and final status. Take Screenshot 12 of SonarQube analysis and quality gate.

## 9. Build and push all Docker tags

Enable 'PUSH_DOCKER_IMAGES' and run again. The ten tags are:

~~~text
<dockerhub-user>/aceest-fitness:1.0.0
<dockerhub-user>/aceest-fitness:1.1.0
<dockerhub-user>/aceest-fitness:1.1.2
<dockerhub-user>/aceest-fitness:2.0.1
<dockerhub-user>/aceest-fitness:2.1.2
<dockerhub-user>/aceest-fitness:2.2.1
<dockerhub-user>/aceest-fitness:2.2.4
<dockerhub-user>/aceest-fitness:3.0.1
<dockerhub-user>/aceest-fitness:3.1.2
<dockerhub-user>/aceest-fitness:3.2.4
~~~

The acceptance failure does not prevent the 3.0.1 Docker image from building; the Dockerfile performs syntax packaging, while Jenkins performs the intentional acceptance gate.

Manual equivalent:

~~~bash
while read -r version; do
  docker build --build-arg APP_VERSION="$version" \
    --tag "<dockerhub-user>/aceest-fitness:$version" .
  docker push "<dockerhub-user>/aceest-fitness:$version"
done < <(python3 -c 'import json; print("\n".join(x["version"] for x in json.load(open("ci/version_manifest.json"))))')
~~~

Take Screenshot 13 of Docker Hub with all ten tags. Take Screenshot 14 of 'docker images' showing all ten tags.

Run the final image:

~~~bash
docker run --rm -d --name aceest-324 -p 8000:8000 \
  -e ACEEST_VERSION=3.2.4 \
  -e ACEEST_SOURCE_VERSION=3.2.4 \
  "<dockerhub-user>/aceest-fitness:3.2.4"
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/version
docker stop aceest-324
~~~

Take Screenshot 15 showing the container and '/health' response.

## 10. Deploy to Kubernetes

Start Minikube or use the approved cloud cluster:

~~~bash
minikube start
kubectl get nodes
kubectl apply -f k8s/namespace.yaml
./scripts/deploy.sh rolling 3.2.4 <dockerhub-user>/aceest-fitness
kubectl get pods,svc -n aceest -o wide
kubectl rollout status deployment/aceest-rolling -n aceest
~~~

For Minikube:

~~~bash
minikube service aceest-rolling -n aceest --url
~~~

For a cloud LoadBalancer:

~~~bash
kubectl get svc aceest-rolling -n aceest -w
~~~

Check the endpoint:

~~~bash
curl http://<cluster-endpoint>/health
curl http://<cluster-endpoint>/api/version
~~~

### 10.1 Rolling update and rollback

~~~bash
./scripts/deploy.sh rolling 3.2.4 <dockerhub-user>/aceest-fitness
kubectl rollout history deployment/aceest-rolling -n aceest
kubectl rollout status deployment/aceest-rolling -n aceest
kubectl rollout undo deployment/aceest-rolling -n aceest
kubectl rollout status deployment/aceest-rolling -n aceest
~~~

### 10.2 Blue-green deployment

~~~bash
./scripts/deploy.sh blue-green 3.2.4 <dockerhub-user>/aceest-fitness
kubectl get deployments,pods,svc -n aceest -l app=aceest
kubectl patch service aceest-blue-green -n aceest \
  -p '{"spec":{"selector":{"app":"aceest","track":"green"}}}'
~~~

The service initially selects blue. Switch to green only after validating green. Roll back by selecting blue:

~~~bash
kubectl patch service aceest-blue-green -n aceest \
  -p '{"spec":{"selector":{"app":"aceest","track":"blue"}}}'
~~~

### 10.3 Canary release

~~~bash
./scripts/deploy.sh canary 3.2.4 <dockerhub-user>/aceest-fitness
kubectl get pods -n aceest -l app=aceest
kubectl get svc aceest-canary -n aceest
kubectl scale deployment/aceest-canary -n aceest --replicas=0
~~~

Use an ingress/controller or request logs to prove the small canary exposure, then promote only after validation.

### 10.4 Shadow deployment

~~~bash
./scripts/deploy.sh shadow 3.2.4 <dockerhub-user>/aceest-fitness
kubectl get deployment,svc -n aceest -l release=shadow
~~~

Shadow traffic requires an ingress controller or service mesh that mirrors production requests to 'aceest-shadow'. Capture the mesh/ingress route and a request log. A shadow Deployment alone is not proof of mirrored traffic.

### 10.5 A/B testing

~~~bash
./scripts/deploy.sh ab-testing 3.2.4 <dockerhub-user>/aceest-fitness
kubectl get deployments,svc -n aceest -l app=aceest
~~~

Use an ingress controller, cookie, header, or separate path to route users to variants A and B. Capture requests reaching both services and roll back by routing all traffic to the stable variant.

Take Screenshot 16 showing Kubernetes pods, services, and endpoint. Take Screenshot 17 showing a strategy transition and rollback. For shadow and A/B, include ingress/service-mesh routing evidence.

## 11. Final checks and report

~~~bash
git status
git log --oneline --decorate --all
git tag --list 'app-v*' | sort -V
git remote -v
~~~

The working tree should be clean, all ten versions should exist, and the GitHub repository should be public or shared with the evaluator.

Complete 'report/SHORT_REPORT_TEMPLATE.md' with your name, student ID, repository URL, endpoint URL, challenges, mitigation, outcomes, and screenshot references.

Final submission evidence:

- GitHub repository link.
- Project ZIP or repository export.
- Completed 2–3 page report.
- Jenkins stages showing every version and the intentional 3.0.1 failure.
- Pytest/JUnit results.
- SonarQube quality gate.
- Docker Hub repository with all ten tags.
- Kubernetes endpoint.
- Deployment strategy and rollback evidence.

## Troubleshooting

### The expected failure stops the pipeline

Confirm that only 3.0.1 is inside the 'catchError' block in 'Jenkinsfile'. Do not wrap all stages in 'catchError'; that would hide real failures.

### Jenkins cannot run Docker

~~~bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
sudo -u jenkins docker version
~~~

### SonarQube cannot be reached

Check the address from the Jenkins agent. '127.0.0.1' means the Jenkins host/container itself, not the developer laptop.

### Kubernetes image pull fails

~~~bash
kubectl describe pod <pod-name> -n aceest
kubectl get events -n aceest --sort-by=.lastTimestamp
~~~

### Tests fail

~~~bash
ruff check .
pytest -q
python3 ci/run_version_matrix.py --allow-expected-failure
~~~

Fix unexpected failures before taking final screenshots. The expected 3.0.1 acceptance failure must remain visible and documented.

