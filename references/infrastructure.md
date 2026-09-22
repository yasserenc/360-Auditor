# Infrastructure, Configuration, and Networking Audit

Use this reference for servers, operating systems, services, web stacks, containers, cloud configuration, networking, DNS, firewalls, routing, deployments, and infrastructure-as-code/configuration.

## Establish the exact target

Identify actual host/resource/environment, OS/distribution, service/software versions, deployment model, network topology, privilege model, persistence mechanism, and production/staging context. Bind evidence to the target actually inspected.

A generic configuration that is valid elsewhere may be wrong in the actual environment.

## Validate relevant layers

Check, as applicable:

- syntax/schema and active configuration;
- version/platform compatibility and prerequisites;
- users, ownership, permissions, authentication, authorization, secrets, trust boundaries, and least privilege;
- service dependencies and startup ordering;
- addresses, interfaces, routes, gateways, DNS, ports, listeners, NAT, proxies, TLS, firewall/security-group paths;
- exposure to public/untrusted networks;
- persistence across reload/restart/reboot;
- resource limits, disk, memory, CPU, file descriptors, connection pools, queues, and capacity assumptions;
- logs, metrics, traces, health checks, and observable failure signals;
- rollback/recovery and backup implications;
- interactions between application/service/database/network layers.

## Direct verification when access exists

Prefer read-only inspection of the real environment when it materially improves confidence. Use independent postcondition signals where possible, for example:

- configuration validator **and** active configuration;
- service/process/listener state **and** expected protocol/application behavior;
- DNS record **and** resolver result;
- firewall rule **and** actual permitted/blocked connection behavior;
- deployment status **and** health/error/user-flow state;
- persisted file/unit **and** later reload/restart behavior when safe and authorized.

Do not restart/reboot merely to prove persistence when consequential action is not separately authorized. Classify material persistence as a Verification-Dependent Risk instead.

If decisive runtime behavior is hidden, seek an evidence bridge such as logs, metrics, traces, health endpoints, read-only queries, or externally observable behavior.

## Command/deployment success is not outcome success

A successful restart, API response, shell exit code, cloud deployment banner, or pipeline completion is an intermediate observation. Verify intended functionality, relevant health, and side effects before using **End-state verified**.

For performance/capacity claims, establish a baseline and measure before/after when feasible; do not label a configuration faster or more efficient from plausibility alone.

## Networking-specific checks

Trace the path in both directions when relevant: source → local host/network policy → routing/NAT → destination listener/service → return path. Distinguish name resolution, reachability, transport, TLS, protocol/application, and authorization failures rather than collapsing them into “network issue.”
