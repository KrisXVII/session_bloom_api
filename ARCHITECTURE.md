# SessionBloom — Architecture

Personal project: Flask backend + Electron/React desktop frontend (being rewritten from Flutter), self-hosted on a Raspberry Pi, split across three repos.

## Read this first — the two expensive gotchas

These two facts cost the most debugging time on the project. Neither is visible in the code that depends on them.

1. **Registration bypasses Kratos self-service hooks.** Identities are created via the Kratos Admin API (`POST /admin/identities`), which means no verification email fires automatically. The backend must explicitly drive the public verification flow afterwards. This is the single most important non-obvious fact about the auth flow.
2. **`Accept: application/json` is required on every Kratos call.** Without it, Kratos answers browser-style with a `303` redirect to a UI URL. This is why `ApiClient._request` sets the header globally in `lib/api_client.py` — do not remove that default.

## Repos

| Repo | Stack | Contents |
| --- | --- | --- |
| `session_bloom_api` | Flask, Python 3.13 | Backend + all infra (compose, Caddyfile, Kratos config) |
| `sessionbloom_desktop` | Electron + React + TypeScript (rewrite from Flutter in progress) | Desktop app (not mobile/web) |
| `beacon` | Go | Small error-alert microservice (learning project) — `/Users/cristianradulescu/Projects/beacon` |

## Runtime topology

```
Electron client ──HTTPS(443)──▶ Caddy ──http──▶ Flask :5000 ──http──▶ Kratos :4433/:4434
                                  (sole ingress)   (internal docker bridge: ory_network)
```

- Only ports 22 and 443 are exposed externally (verified by nmap). SSH is ed25519 key-only + fail2ban + ufw.
- Kratos public `:4433` and admin `:4434` are bound to `127.0.0.1` — reachable only from the Pi. Hydra `:4444`/`:4445` likewise.
- Flask publishes no ports; it is reachable only through Caddy.
- `api.sessionbloom.z` — deliberately fake TLD, resolves only on the local network. Doubles as a placeholder keeping any future real domain out of version control.
- Local Kratos access for debugging and fixture capture is via SSH tunnel, never by opening ports.

## Auth — Kratos only

Backend-mediated: the desktop client never talks to Kratos directly (it can't — Kratos is localhost-bound). Flask proxies every Kratos call.

- Ory Kratos v1.3.0, self-hosted. Identity schema: `email` (marked `credentials.password.identifier`, with verification + recovery via email), `first_name`, `last_name`.
- **Password policy:** min length 10 (matched in both the Kratos config and the Marshmallow schema), HaveIBeenPwned breach check enabled. No composition rules — deliberate, following NIST SP 800-63B.
- **Registration** creates identities via the Kratos Admin API (`POST /admin/identities`). See gotcha #1 above: this bypasses self-service hooks, so the backend explicitly drives the public verification flow afterwards.
- **Verification** uses the `code` method (6-digit), not `link` — chosen because links get consumed by email scanners and a desktop app has no sensible browser landing page. Flow:
  1. `GET /self-service/verification/api`
  2. `POST ?flow=<id>` with `{method, email}`
  3. `POST ?flow=<id>` with `{method, code}`
- **Verify-first model:** no `session` hook on registration, so signup issues no session. Note that Kratos still allows unverified users to log in (soft verification); a hard gate would need `require_verified_address`. Not currently enforced.
- **Login** uses the Kratos native/API flow (not browser): `GET /self-service/login/api` → `POST /self-service/login?flow=<id>` with `{method: "password", identifier, password}`. Both calls happen server-side within one request; the flow id never reaches the client.
- **Sessions** use opaque tokens, not JWT. Deliberate: instant revocation, no local crypto to implement, and it avoids the JWT vulnerability family (`alg:none`, HS256/RS256 confusion). Validated by calling Kratos `/sessions/whoami`, never decoded locally. Sessions persist in Kratos's `sessions` table — that persistence is what makes revocation possible.
- **Session lifespan:** currently the Kratos default (24h); no `session:` block is configured. Sliding sessions (`lifespan` + `earliest_possible_extend`) are the intended fix.
- **Anti-enumeration is a hard requirement.** `notify_unknown_recipients: false`, and login errors must stay generic. Kratos returns the same message for "no such email" and "wrong password" — that must not be un-flattened.
- **Hydra** is present in compose but dormant. Not part of the auth path.
- **Planned:** Google/Apple via Kratos `oidc`, on a separate endpoint since OIDC needs a browser hop + deep-link callback.
- **Known issue:** profile edits currently go through the Admin API with a caller-supplied `user_id` → IDOR risk. The correct fix is Kratos's self-service settings flow (identity derived from the session token, no tamperable target). `privileged_session_max_age: 15m` is already configured for it.

## API-client layer (mirrored on both sides)

A deliberate "Faraday-style" pattern, implemented twice.

**Backend** — `lib/api_client.py`: `ApiClient(base_url)` wraps a `requests.Session`. The `get`/`post`/`put`/`patch`/`delete` methods are sugar over `_request(method, path, expected=(200, 201), error_message=..., **kwargs)`. It defaults `Accept: application/json` globally (see gotcha #2). Transport failure → `CustomError(503)`; unexpected status → `CustomError(error_message, status)`. One instance per base URL (`KratosAdminAPI`, `KratosPublicAPI`).

**Frontend** — being rebuilt in TypeScript. The Flutter implementation (`DioClient` → `ApiClient` → `safeApiCall`, with the rule that widgets never import Dio) is retired. The intent carries over: one HTTP client module that components go through instead of calling `fetch` directly, translating every transport or HTTP failure into a single `ApiError` type. Library choice still open.

## Data

- PostgreSQL self-hosted on the Pi; Neon for cloud Postgres (chosen over Supabase for scale-to-zero, EU Frankfurt, and free branching).
- Alembic migrations, run from the CI deploy job.
- Domain models: `User`, `Session`, `SubSession`, `SessionDescription`, `Counter`.
- `User.kratos_id` is the join between Kratos identities and local user rows.
- ⚠️ **Naming collision:** the domain `Session` (time tracking, the product's core feature) is unrelated to a Kratos auth session. Different databases, different lifecycles.
- Authorization is application-side. Kratos answers "who is this"; scoping every query to the authenticated owner is the app's job.

## Email

- Resend (cloud SaaS) via Kratos's courier SMTP — `smtps://resend:${RESEND_TOKEN}@smtp.resend.com:465/`. Token lives in a gitignored `.env`; the URI is composed in compose.
- Dev sender is `onboarding@resend.dev`, which only delivers to the account owner's address. Production needs a registrable domain + SPF/DKIM/DMARC.
- Kratos template overrides (`courier.template_override_path`) are available for custom email content.

## Error tracking & alerting — two independent pipelines

**PostHog** (chosen over Sentry, free tier) captures exceptions for its own dashboard and analytics. It runs entirely on its own and is not part of the Slack alert path.

**Beacon** is a purpose-built alert pipeline, decoupled from PostHog on purpose:

1. Flask registers a single global error handler (`@app.errorhandler(Exception)`) that catches every uncaught exception across all routes.
2. The handler filters out expected HTTP errors (404s, 400s, anything Flask/Werkzeug already handles normally) — only genuine unhandled crashes get forwarded.
3. Flask POSTs the error payload directly to Beacon over the local network/LAN — no public internet exposure needed for either service.
4. Beacon validates the payload, then checks an in-memory map to deduplicate/rate-limit repeated instances of the same error within a short window.
5. Beacon formats a Slack message and POSTs it to a Slack Incoming Webhook.
6. Beacon returns 200 to Flask to acknowledge receipt.

The two pipelines never touch: Beacon receives directly from Flask (step 3) and does not tail PostHog. Transport is a plain HTTP POST from Flask over the LAN, acknowledged with a 200 (steps 3 and 6).

**Known gap — Beacon cannot detect a dead Flask.** Since Flask is the only reporter, Beacon can only alert on exceptions inside a *running* Flask. It cannot tell you when Flask is dead: OOM-killed, crashed on boot, container down, or the Pi offline. Those are exactly the failures most worth a Slack message, and the current design is silent on all of them. See open decisions below.

## i18n

- **Frontend:** mechanism to be chosen for the React rewrite. The Flutter ARB setup (`app_en.arb`, `app_it.arb`) is retired; English and Italian remain the target locales.
- **Backend:** Flask-Babel planned, not implemented.
- **Decision:** the backend owns error-message localization (client sends `Accept-Language`); the frontend owns success copy. Pure network/timeout errors stay client-side.
- Kratos's own English messages must never be relayed to the client — curate them, or map Kratos's stable numeric message IDs to our own strings.

## CI/CD

- GitHub Actions (`dev_api_deploy.yml`): a `test` job on `ubuntu-latest`, and a `build` job on a self-hosted runner on the Pi (`needs: test`, `dev` branch only).
- Deploy job: checkout → venv → write `.env` from GitHub Secrets → `alembic upgrade head` → `docker compose up -d --build` → `docker image prune`.
- The backend image bakes the code (`build: .`); a `.:/app` volume + `FLASK_DEBUG=1` is used for live reload in dev.

## Testing

- pytest, with `UserFactory`, Faker, and Marshmallow schemas as response contracts (`assert_valid_schema` — `unknown=RAISE` doubles as a guard against accidental field leakage).
- Kratos is stubbed at the HTTP layer with the `responses` library. JSON fixtures live in `tests/stubs/json_responses/`, captured from a real Kratos via SSH tunnel — scrub the email field before committing.
- **Convention:** unit tests assert the *outbound request* (`responses.calls[0].request`), not the canned fixture. Integration tests assert local DB effects plus that params reached Kratos correctly.

## Security posture (explicit project goal)

- Curated responses everywhere — never relay upstream (Kratos) bodies to the client. Log the raw detail, return a controlled message.
- Client-side logging must redact credentials and be stripped from release builds. The Flutter version enforced this with `kDebugMode`; the React build needs an equivalent.
- Secrets: gitignored `.env` + GitHub Secrets. TLS keys are bind-mounted read-only, never baked into images. FileVault on the dev machine.
- The Kratos Admin API is never internet-exposed.

## Open / parked decisions

**Error tracking**

- Exact Flask → Beacon payload shape — still to be defined.
- Beacon's dedup window and thresholds — not yet decided.
- Linking the Slack alert back to the matching PostHog issue (Sentry-style) — parked; will need Flask to pass through whatever identifier Beacon can use to build that link.
- Out-of-band liveness signal, to cover the dead-Flask gap above. Beacon expecting a periodic heartbeat and alerting on its absence is the usual cheap fix, and it inverts the dependency nicely.

**Auth & API**

- Endpoint protection via `whoami` — not implemented. No route currently authenticates. This is the next milestone after the PostHog/Beacon work.
- Rate limiting — not implemented. Planned order: a per-email limit in Flask on `send_verification_code` first (it triggers real outbound email → quota burn + mail-bombing), then Caddy per-IP (needs the `mholt/caddy-ratelimit` module via xcaddy, as Caddy has no built-in limiter), then fail2ban.
- Profile settings flow to replace the admin-API route (IDOR).
- Session lifespan / sliding-session config.
- Whether to hard-gate login on verified email.
- Cron to purge unverified identities — must delete from both Kratos (admin API) and the local DB, or they drift.

**Infra & hardening**

- Debug output on the Pi. `create_app` falls back to `config['default']` (= `DevelopmentConfig`, `DEBUG = True`) for any unrecognised `FLASK_ENV`, silently. Combined with Caddy as a public ingress on 443, that renders full tracebacks and the Werkzeug console to callers — contradicting the curated-response rule. Open: fail loudly on an unknown `FLASK_ENV`, and decide whether the Pi wants a fourth mode (real endpoints, live reload, debug output off).
- Docker socket access on the Pi. The API container runs as `appuser`, but `docker exec -u root` needs no authentication — expected, since Docker daemon access is root-equivalent on the host by design. The real boundary is who can reach the socket: SSH users plus anyone in the `docker` group. The self-hosted Actions runner has Docker access, so anything that makes it execute arbitrary code gets host root. `USER appuser` still earns its place — it limits blast radius from RCE through Flask.
- Self-hosted runner exposure — **currently contained, and worth keeping that way.** The repo is public, but `dev_api_deploy.yml` triggers only on `push` to `dev` (no `pull_request`, `pull_request_target`, or `workflow_dispatch`), so fork-originated code cannot reach the runner; that requires write access to the repo. ⚠️ Adding any fork-reachable trigger to a workflow that runs on `self-hosted` would remove this protection. Open: confirm the runner is registered repo-scoped rather than account-scoped, and pin `actions/checkout` to a commit SHA rather than the moving `@v6` tag (it is the only third-party code running on the Pi as the Docker-capable runner user).
- The deploy-generated `.env` persists in the runner workspace between runs (runner is not ephemeral), putting every secret on disk alongside Docker access.
- Image contains `nano` and `bash` — dev convenience, post-exploitation convenience in production. Candidate for a multi-stage or slimmed production image.

**Frontend & distribution**

- **Rewrite from Flutter to Electron + React + TypeScript** (decided September 2026; Flutter felt too heavy). Tooling proposed, not yet locked in: Vite (via `electron-vite` or Electron Forge) rather than Next.js, whose server-side features go unused in Electron; Tailwind + shadcn/ui for styling; native `vibrancy` (macOS) and `backgroundMaterial` (Windows 11) for window translucency, with a CSS fallback on Linux.
- Electron hardening baseline to adopt from the first commit: `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`, a preload script exposing a narrow API through `contextBridge`, and a strict CSP. Store the Kratos session token with `safeStorage` (OS keychain), never `localStorage`.
- The desktop client authenticates users with Kratos session tokens. It must not hold an OAuth client secret: an Electron bundle is readable JavaScript, the same reason application-layer encryption is rejected below. Hydra `client_credentials` is for service-to-service calls only.
- Client distribution via GitHub Releases, built per OS (macOS signing and notarisation need a Mac). Code signing unresolved (Apple Developer $99/yr; Windows SmartScreen) — still the genuinely hard part.

**Decided against**

- Application-layer body encryption. TLS covers it, and an open-source distributed client can't hold a key secretly.
