# Step V-03: Density Validation

## Goal
Validate document meets information density standards by scanning for filler and wordy phrases.

## Anti-Pattern Checks

Scan for these categories:

### Conversational Filler
- "The system will allow users to..." → should be "Users can..."
- "It is important to note that..." → remove entirely
- "In order to..." → replace with "To..."
- "At the end of the day..." → remove
- "Due to the fact that..." → "Because..."

### Wordy Phrases
- "In the event of" → "If"
- "As a matter of fact" → "Actually" or remove
- "A large number of" → "Many"
- "In regards to" → "Regarding" or "About"

### Redundant Expressions
- "Future plans" → "Plans"
- "Past history" → "History"
- "Unexpected surprise" → "Surprise"
- "Current status" → "Status"

## Severity Classification

**Critical (>10 violations):**
- Document is bloated with filler
- Signal-to-noise ratio is poor
- Requires significant rewrite for clarity

**Warning (5-10 violations):**
- Some wordiness present
- Moderately impacts readability
- Can fix with targeted editing

**Pass (<5 violations):**
- Density meets standards
- Each sentence carries weight
- Ready to proceed

## Execution

1. Scan entire document for anti-patterns
2. Count violations per category
3. Document line numbers and specific violations
4. Classify severity
5. Auto-proceed to next step

## Append to Report

```
## Density Validation (Step 3)

**Anti-Patterns Found:** {count}

### Conversational Filler
- Line X: "The system will allow users to..." → Suggestion: "Users can..."
- Line Y: "It is important to note that..." → Suggestion: Remove

### Wordy Phrases
- Line Z: "In the event of" → Suggestion: "If"

**Severity:** {CRITICAL | WARNING | PASS}
**Status:** ✓ Proceeding to Brief Coverage Validation
```

## Next Step

→ Execute `step-v-04-brief-coverage-validation.md`
