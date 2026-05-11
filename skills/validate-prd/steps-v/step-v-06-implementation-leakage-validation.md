# Step V-06: Implementation Leakage Validation

## Goal
Ensure FRs and NFRs specify WHAT (capability), not HOW (implementation). Technology names and infrastructure details don't belong in requirements.

## Why This Matters
Requirements that include implementation details lock the team into specific technology choices before design and architecture work begins. A requirements/design document should describe capabilities that any reasonable implementation could fulfill — the "how" is decided during architecture planning.

## Process

### 1. Locate Requirements Sections

Scan these sections of the document:
- Functional Requirements
- Non-Functional Requirements
- Game-specific sections that contain requirements (balance targets, performance targets)

Do NOT scan: User Journeys or Scope (implementation terms there may be contextually appropriate).

### 2. Scan for Implementation Terms

Search for these terms within requirements sections:

**Frontend Frameworks:**
React, Vue, Angular, Next.js, Svelte, Nuxt, Remix, Ember

**Backend Frameworks:**
Express, Django, Rails, Spring, Laravel, FastAPI, Flask, NestJS

**Game Engines (in requirements — OK in Technical section, NOT in FRs/NFRs):**
Unity, Unreal, Godot, GameMaker, CryEngine, Lumberyard

**Databases:**
PostgreSQL, MySQL, MongoDB, Redis, DynamoDB, SQLite, Cassandra, Firebase

**Cloud Platforms:**
AWS, GCP, Azure, Vercel, Render, Cloudflare, Netlify, Heroku, Fly.io

**Infrastructure:**
Docker, Kubernetes, Terraform, Ansible, Nginx, Apache

**Libraries & Tools:**
Photon, Mirror, ENet, MLAPI (networking libs), Addressables, PlayFab, GameSparks

**Data Formats (when used as implementation detail):**
JSON, XML, YAML (acceptable when describing data exchange capability, not implementation)

### 3. Evaluate Each Match: Leakage vs. Capability-Relevant

Not every technology mention is a violation. Evaluate context:

**Capability-Relevant (NOT a violation):**
- "Players can export save data in a portable format" (format unspecified)
- "API consumers can access game data via standard web protocols" (protocol not named)
- "Game supports cross-platform saves" (platform-agnostic)

**Implementation Leakage (IS a violation):**
- "Game uses Unity's Addressables system for asset loading"
- "Player data stored in MongoDB with Redis cache"
- "Multiplayer handled via Photon PUN2"
- "Save files exported as JSON"

**Edge case — game engine in platform requirements:**
- Acceptable: "PC build targets Windows 10+ (x64)" — platform, not engine
- Leakage: "Built with Unity 2022 LTS targeting Windows" — engine choice in FR

### 4. Count and Classify

Count confirmed leakage violations (not capability-relevant mentions).

**Critical (>5 violations):**
- Requirements are tightly coupled to implementation
- Architecture decisions are constrained by the document
- Significant rework needed

**Warning (2-5 violations):**
- Some implementation bias present
- Architecture team should review flagged FRs
- Recommend revising before development

**Pass (<2 violations):**
- Requirements are capability-focused
- Architecture team has freedom to choose best implementation

## Append to Report

```
## Implementation Leakage Validation (Step 6)

**Sections Scanned:** Functional Requirements, Non-Functional Requirements, Game Mechanics
**Violations Found:** {count}

### Violations
- Line X: "...stored in MongoDB..." → Suggest: "...stored in persistent game database..."
- Line Y: "...using Photon for sync..." → Suggest: "...synchronized via dedicated game server..."
- Line Z: "...Unity Addressables..." → Suggest: "...dynamic asset streaming system..."

### Capability-Relevant Mentions (Not Violations)
- Line A: "...standard web protocols..." — OK, no specific technology named

**Severity:** {CRITICAL | WARNING | PASS}
**Status:** ✓ Proceeding to Game Compliance Validation
```

## Output

- ✓ All requirements sections scanned
- ✓ Technology terms identified and evaluated
- ✓ Violations distinguished from capability-relevant mentions
- ✓ Specific replacement suggestions provided
- ✓ Findings appended to report

## Next Step

→ Execute `step-v-07-game-compliance-validation.md`

## Important Constraints

- **Do NOT** load step-v-07 before completing this step
- **Do NOT** modify the document
- **Do** evaluate context before flagging — not all tech mentions are violations
- **Do** provide a capability-level rewrite suggestion for each violation
