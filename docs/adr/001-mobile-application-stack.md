# ADR-001 — Mobile Application Stack

**Decision status:** Accepted  
**Implementation status:** VERIFIED IN REPLIT V1

## Context

The Buyer Agent requires a cross-platform mobile experience with Android
as the initial target and web preview capability during development.

The current application is TypeScript-first and shares a workspace with
a Node.js API server.

## Decision

Use:

- Expo
- React Native
- TypeScript
- pnpm monorepo
- Expo Router

## Alternatives Considered

- Native Android
- Separate Android and iOS applications
- Flutter
- React web wrapped for mobile

## Rationale

This provides a single codebase across Android, iOS and web while reducing
native build complexity during prototyping.

pnpm workspaces also allow application and server packages to coexist and
share code.

## Consequences

- Some native capabilities may require Expo development builds.
- React Native Web has behavioral differences from React DOM.
- Platform-specific testing remains necessary.

## Verification

Replit verified this implementation in:

- `artifacts/buyer-agent/app.json`
- `babel.config.js`
- `metro.config.js`
- `tsconfig.json`
- `pnpm-workspace.yaml`
- Expo Router files under `app/`
