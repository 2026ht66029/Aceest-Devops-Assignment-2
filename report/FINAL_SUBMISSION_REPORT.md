# ACEest Fitness and Gym — DevOps Assignment 2

**Student ID:** s2026ht66029  
**Repository:** https://github.com/2026ht66029/Aceest-Devops-Assignment-2

## CI/CD architecture overview

GitHub is the source repository and Jenkins continuously polls `main` using `H/5 * * * *`. The pipeline checks out the project, creates the Python environment, builds and validates all ten supplied versions, records only version `3.0.1` as the intentional acceptance regression, runs Pytest/JUnit and SonarQube, builds ten Docker tags, pushes them to the approved local registry, and deploys the selected Kubernetes strategy in Minikube.

Flow: **GitHub → Jenkins → version matrix → Pytest/SonarQube → Docker tags → `localhost:5000/aceest-fitness` → Kubernetes → health/version verification**.

## Automation outcomes

- Ten milestone versions are preserved under `versions/` and represented by `app-v*` tags.
- Jenkins build #22 completed all non-intentional stages. The expected `3.0.1` regression made the build `UNSTABLE`; later versions continued.
- Pytest: 15 tests passed; coverage: 92.47%.
- SonarQube project `aceest-fitness-multiversion`: quality gate **Passed**.
- All ten image tags were verified in `localhost:5000/aceest-fitness`.
- Minikube namespace `aceest` contains the rolling, blue-green, canary, shadow and A/B resources.

## Deployment strategies

| Strategy | Demonstration |
|---|---|
| Rolling / rollback | Rollout history, `rollout undo`, and restored READY state verified for `aceest-rolling`. |
| Blue-green | `aceest-blue-green` service switched blue → green → blue and was restored. |
| Canary | Stable and canary deployments/services used separate selectors and endpoint pools. |
| Shadow | Stable and shadow services returned healthy responses to the same client-side mirrored-request demonstration. |
| A/B | Variant-A and variant-B services returned separate `/api/version` responses. |

Shadow and A/B evidence is described at the service/request demonstration level; no unverified service-mesh behavior is claimed.

## Challenges and mitigation

The intentionally failing `3.0.1` gate is isolated with `catchError` so real failures remain visible. Docker Hub was replaced by the permitted local registry alternative because the live Docker Hub credential path was unavailable. Jenkins/SonarQube host networking was configured for the lab VM, and separate Kubernetes manifests/services isolate each deployment strategy.

## Required project contents and submission references

The project contains `ACEest_Fitness.py`, `app.py`, `versions/`, `Jenkinsfile`, `Dockerfile`, `k8s/`, `tests/`, CI scripts, and `sonar-project.properties`. The running Minikube endpoint can be reproduced with:

```bash
kubectl -n aceest port-forward service/aceest-stable 18080:80
curl http://127.0.0.1:18080/health
```

The accompanying submission package contains the project ZIP, the formatted 3-page report, detailed evidence report, and live screenshots.
