# adr-creator

Small util tool to create adr form the command line

## Check out

- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- https://martinfowler.com/bliki/ArchitectureDecisionRecord.html

## Facts

- --- terminates multi-line input sections
- ADR numbers are auto-incremented
- Filenames are slugified automatically
- CLI flags skip interactive prompts where possible

## Example

```Bash
$ adr
======================================================================
ADR Creator
======================================================================
Using directory: ./docs/adr
Found 3 ADRs. Suggested next number: 0004

ADR number [0004]:
Title: Use HTMX for Server-Driven UI
Author [Nick]:
Status (proposed/accepted/superseded) [proposed]: accepted

## Context
(Finish with '---' on a new line)
We want to reduce frontend complexity and avoid a heavy SPA framework.
The team prefers server-side rendering with minimal JavaScript.
---

## Decision
(Finish with '---' on a new line)
We will adopt HTMX to enable server-driven UI updates via HTML over the wire.
---

## Consequences
(Finish with '---' on a new line)
Pros:
- Less JavaScript complexity
- Faster development

Cons:
- Less control over client-side interactions
---

ADR created:
docs/adr/0004-use-htmx-for-server-driven-ui.md
```
