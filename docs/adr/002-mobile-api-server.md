# ADR-002 — Mobile API Server

**Decision status:** Accepted  
**Implementation status:** VERIFIED IN REPLIT V1

## Context

The mobile experience requires server-side access to external services,
including product enrichment and voice capabilities.

Calling these services directly from the mobile client would introduce
credential, CORS and integration concerns.

## Decision

Use an Express.js TypeScript API server under:

`artifacts/api-server`

Bundle it using esbuild.

Current V1 capabilities include:

- product image lookup
- speech-to-text
- text-to-speech

## Alternatives Considered

- Direct third-party API calls from the mobile client
- Serverless functions
- Separate backend service
- Python service for all mobile endpoints

## Rationale

The API server centralizes external integrations and prevents service
credentials from being embedded in the client.

## Consequences

- The mobile application depends on server availability.
- Native and web environments require appropriate API base URLs.
- Additional backend capabilities may eventually be separated into
  dedicated services.
