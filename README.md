# SessionBloom

SessionBloom — a productivity app for designing custom focus sessions: the user takes a block of time, partitions it into work/break sub-blocks as they like, starts a timer, and the app runs the sequence automatically with audio cues at each transition.
This repo is the backend + infrastructure. Built as a personal project to practice production-grade patterns and best practices.
Stack: Flask · PostgreSQL · Docker (self-hosted) · mTLS · Ory Kratos & Hydra (identity/auth).
Why the architecture is heavier than the app needs: deliberately — the goal was hands-on practice with secure auth flows, containerized self-hosting, and clean API design, not just a working timer.
