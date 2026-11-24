# Assignment 2 Screenshot Checklist

Take screenshots only after the command or web page is complete. Crop terminal/browser address bars when they contain access tokens, session tokens, passwords, or unrelated personal data.

| ID | Evidence | Where to capture | Must show |
| --- | --- | --- | --- |
| 1 | Package extraction | Linux terminal | Project directory and top-level files |
| 2 | All-version local matrix | Terminal | All ten versions, intentional 3.0.1 failure, later passes |
| 3 | Unit tests | Terminal/Jenkins | Pytest result and coverage |
| 4 | Local API | Terminal/browser | `/health` and `/api/version` |
| 5 | GitHub repository | GitHub Code tab | Jenkinsfile, Dockerfile, versions, ci, tests, k8s |
| 6 | Git history/tags | Terminal or GitHub | All milestone tags and structured commit history |
| 7 | Jenkins configuration | Jenkins job configuration | SCM repository and Jenkinsfile path; hide credentials |
| 8 | SonarQube configuration | SonarQube/Jenkins | Project and quality gate; hide tokens |
| 9 | Jenkins stage view | Jenkins build | Red Validate 3.0.1, green later version stages |
| 10 | Jenkins console | Jenkins console | Intentional failure reason and later successful stages |
| 11 | Jenkins tests | Jenkins test report | JUnit/Pytest results and final UNSTABLE status |
| 12 | SonarQube result | SonarQube dashboard | Analysis date, measures, quality gate |
| 13 | Docker Hub | Docker Hub tags | All ten application tags |
| 14 | Local Docker images | Terminal | All ten version tags |
| 15 | Runtime container | Terminal/browser | Running container and `/health` response |
| 16 | Kubernetes endpoint | Terminal/browser | Pods, service, external/Minikube URL, API response |
| 17 | Deployment and rollback | Terminal/Kubernetes dashboard | Strategy switch and rollback result |

For Shadow Deployment and A/B Testing, add an extra screenshot showing the ingress/service-mesh route or request evidence. A list of Pods alone does not prove traffic mirroring or traffic splitting.

Before submission, verify that no screenshot contains a GitHub token, Docker Hub token, SonarQube token, SSH private key, remote desktop token, or password.
