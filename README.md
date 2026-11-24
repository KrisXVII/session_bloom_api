# SessionBloom

> A productivity app for designing custom focus sessions — take a block of time, partition it into work and break sub-blocks however you like, hit start, and let it run.

The user picks a chunk of time (say, 2 hours), splits it into sub-blocks as they please — e.g. 60 min focus → 15 min break → the rest on something else — then starts a timer that runs the whole sequence automatically, firing an audio cue at each transition so you know when a block starts or ends.

This repository contains the **backend and infrastructure**. It's a personal project built to practice production-grade patterns and best practices end to end.

---

## Tech stack

| Layer | Technology |
|---|---|
| API | Flask |
| Database | PostgreSQL |
| Auth / Identity | Ory Kratos & Ory Hydra |
| Transport security | mTLS |
| Deployment | Docker (self-hosted) |

## Why the architecture is heavier than the app needs

Deliberately. A session timer doesn't require mutual TLS and a full identity stack — but building one *as if it did* was the point. The goal was hands-on practice with:

- Secure authentication and authorization flows (Ory Kratos for identity, Hydra for OAuth2/OIDC)
- Mutual TLS between services
- Containerized, self-hosted deployment
- Clean, maintainable API design

## Project status

🚧 **Work in progress.** Core session logic and auth are in place; actively developing.

## Related repositories

- **Desktop frontend (Flutter):** https://github.com/KrisXVII/sessionbloom_desktop
