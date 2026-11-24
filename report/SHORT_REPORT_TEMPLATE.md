# ACEest Fitness and Gym CI CD Assignment 2 Report

## Student and repository details

- Student name: `<Your name>`
- Student ID: `<Your ID>`
- GitHub repository: `<Public repository URL>`
- Docker Hub repository: `<Docker Hub URL>`
- Kubernetes endpoint: `<Endpoint URL>`

## 1. CI/CD architecture overview

Describe the flow:

`GitHub -> Jenkins checkout -> version matrix build -> version acceptance -> Pytest -> SonarQube -> Docker image tags -> Docker Hub -> Kubernetes deployment -> health check`

The repository preserves ten supplied ACEest milestones. Jenkins builds every milestone in order. Version 3.0.1 is an intentional acceptance failure and is marked as an expected failed stage; subsequent milestones continue. The Flask delivery layer provides a container-safe API and health endpoint.

## 2. Version and failure design

List the ten versions and explain that `ci/version_manifest.json` is the source of truth. Explain why version 3.0.1 is intentionally failed, how `catchError` records it without hiding later stages, and how the final Jenkins result becomes `UNSTABLE` rather than silently passing.

Attach or reference Screenshot 9 and Screenshot 10.

## 3. Tools and implementation

Explain the use of:

- Git/GitHub for version control, commits, branches, and tags.
- Jenkins for automated staged builds and test reporting.
- Pytest for Flask API and manifest tests.
- SonarQube for static analysis and quality-gate enforcement.
- Docker/Podman for versioned application images.
- Docker Hub for storing all ten image tags.
- Kubernetes/Minikube for deployment and rollback.

Attach or reference Screenshots 5, 6, 11, 12, 13, and 16.

## 4. Deployment strategies and rollback

Summarize the strategy evidence:

- Rolling update: controlled replica replacement with rollout undo.
- Blue-green: Service selector switches between blue and green tracks.
- Canary: stable and canary replica groups share a service during limited exposure.
- Shadow: production requests are mirrored by the ingress/service mesh to a shadow service.
- A/B: routing sends different users or paths to variant A or B.

Explain the rollback command or traffic switch used and the result observed in the health endpoint or rollout status.

Attach or reference Screenshot 17 and the additional Shadow/A-B routing screenshot.

## 5. Challenges and mitigations

Describe actual issues encountered. Examples:

| Challenge | Mitigation |
| --- | --- |
| Tkinter milestones cannot be opened in a headless Jenkins agent | Compile and AST-check the supplied files without launching GUI code; use the Flask delivery layer for container tests |
| One milestone must fail without stopping the version matrix | Use an explicit expected failure entry and wrap only that Jenkins stage with `catchError` |
| Jenkins cannot reach SonarQube on `127.0.0.1` from a container | Configure a reachable service name or host address from the Jenkins agent |
| Kubernetes image is not pullable | Verify Docker Hub tag visibility, image name, and image-pull credentials |

Replace these examples with the actual problems and evidence from your run.

## 6. Automation outcomes

Record the final observed outcomes:

- Number of versions built: `10`
- Intentional failed version: `3.0.1`
- Unexpected failed stages: `<0 or explain>`
- Pytest result and coverage: `<result>`
- SonarQube quality gate: `<PASS/FAIL>`
- Docker Hub tags published: `<10 or explain>`
- Kubernetes endpoint: `<URL>`
- Rollback verified: `<yes/no and command>`

## 7. Conclusion

Conclude how the pipeline demonstrates versioned delivery, automated quality checks, containerized builds, progressive deployment, and recovery after a failed validation or deployment.
