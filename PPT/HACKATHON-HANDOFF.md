# Snowflake Hackathon: AI Handoff and Readiness Guide

## Purpose

This document is the working brief for an AI assistant or teammate helping build a project for the Data in the D 2026 Snowflake hackathon. It summarizes the supplied slide photos, records the rules and submission requirements visible in them, and gives a practical build checklist. Treat event instructions and the organizers' decisions as authoritative if they differ from this summary.

## Event at a glance

- **Event:** AI at Work: Hack the Everyday — Data in the D 2026
- **Date and venue:** Friday, October 16, 2026; Benson & Edith Ford Conference Center, College for Creative Studies, Detroit
- **Official agenda:** <https://www.datainthed.org/2025event-agenda-26#hackathon>
- **Hackathon window on agenda:** 12:15–5:15 PM
- **Devpost deadline shown in supplied slides:** 4:30 PM. Submit before this deadline; do not treat the event's 5:15 PM end time as the submission deadline.
- **Resources described on the agenda:** a 30-day Snowflake trial and three custom challenge datasets
- **Workshop photo:** “Zero to Shipped with CoCo,” 12:00–2:00 PM; it runs alongside the hack, so participants can drop in and return to their team.

The screenshots are photographs of projected slides. There is no `.ppt` or `.pptx` in this folder. Use the original images linked in the [image index](#image-index) if a detail is unclear. Confirm account permissions, available AI capabilities, dataset details, and submission mechanics with event staff rather than assuming a recommended feature is enabled.

## Rules and data guardrails

- Work solo or in a team of up to four; each team enters one track.
- Write the project code during the event. Planning ideas ahead and using open-source libraries are allowed.
- Build on the provided Snowflake account.
- Do not use confidential, regulated, or personal employer data.
- Meet the Devpost deadline; late submissions will not be judged.
- Follow the event's code of conduct and treat participants respectfully.

The event page describes the provided trial and datasets. The slides also show other possible data sources (your own permitted data, Snowflake Marketplace, and synthetic data). The data-safety warning still applies; check with organizers before using any non-provided source.

## Pick the track

Use the supplied slide names and definitions:

| Track | Audience | Deliverable | Choose it when… |
|---|---|---|---|
| **Hack the Question** | Analysts | A visual analysis or report | The main result is an answer, finding, or report; the product does not create, change, or send something. |
| **Hack the Grind** | Engineers | A repeat-use tool | It creates, changes, or sends something and the primary user is you or your team. |
| **Hack the Experience** | Builders | Something an end user actually uses | It creates, changes, or sends something for an end user outside your team, especially someone who does not write SQL. |

Track decision rule from the slide: if the project does not create, change, or send something, choose **Hack the Question**. If it does, choose **Hack the Grind** when the main user is you/your team, otherwise choose **Hack the Experience**.

## What a strong project needs

The slides call out three essentials:

1. A visual component, such as Streamlit, an HTML report, or a dashboard.
2. Snowflake features working together intentionally, not an arbitrary feature checklist.
3. AI doing real work, not merely decorating the interface.

Build one coherent, demonstrable workflow. The slides recommend focusing on a real problem, taking screenshots as you go, and shipping a solid working prototype rather than overclaiming a more complete product.

### Feature ideas shown in the slides

These are suggestions, not guarantees of account availability:

- **Hack the Question:** Semantic Views + Cortex Analyst, Cortex Search, AISQL (such as `AI_COMPLETE`, `AI_CLASSIFY`, `AI_SENTIMENT`), `AI_EXTRACT`, Notebooks, and Marketplace data.
- **Hack the Grind:** Cortex Agents (including a coding agent), Managed MCP, Tasks and Streams, Dynamic Tables, Alerts, Data Metric Functions (DMFs), dbt Projects, CoCo skills, and Openflow.
- **Hack the Experience:** Streamlit, Cortex Agents, Semantic Views, Cortex Search, `AI_TRANSLATE`, and restricted caller rights.
- **All tracks:** the “Every project needs these three things” slide recommends using CoCo to build faster.

Ask the organizers which features are enabled and use only capabilities the team can actually demonstrate.

## Judging criteria

The slide says criterion weights differ by track:

| Criterion | Hack the Question | Hack the Grind | Hack the Experience |
|---|---:|---:|---:|
| Insight Quality | 25% | — | — |
| Communication | 15% | — | — |
| Time Reclaimed | — | 15% | — |
| Reusability | — | 15% | — |
| Experience Quality | — | — | 35% |
| Relevance | — | — | 25% |
| How Baked Is It? | 20% | 20% | 20% |
| Platform Craft | 20% | 30% | 10% |
| Meaningful AI Use | 20% | 20% | 10% |

## “How Baked Is It?” self-score

The slide assigns 20% of every track to this criterion and asks teams to score honestly:

1. **Storyboard:** screens exist, but no logic is behind them.
2. **Happy path:** works only when following the demo script.
3. **Working prototype:** works end-to-end on real data.
4. **Usable by others:** handles bad input.
5. **Handoff-ready:** someone else could use it at work.

The slide notes that most strong projects score a 3 and that an honest 2 can beat an overclaimed 4. State clearly what is real and what is mocked or faked.

## Build and submission checklist

### At the start

- [ ] Check in; confirm team (solo or up to four), team name, and one chosen track.
- [ ] Sign in to the provided Snowflake account and verify access to the challenge datasets.
- [ ] Confirm available roles, AI features, external-service rules, and Devpost submission process with organizers.
- [ ] Inspect the provided datasets and decide on one user, one problem, and one small MVP.
- [ ] Assign owners for data/query work, application/demo, and the pitch.

### Build the MVP

- [ ] Prove one direct Snowflake query and one AI capability against real, permitted data.
- [ ] Create the shortest end-to-end path: data → Snowflake/AI work → useful output → visual component.
- [ ] Compose Snowflake features around the use case; do not add features just to increase the count.
- [ ] Verify important results against the underlying data; show the source/context needed to interpret an AI answer.
- [ ] Keep credentials out of source control and do not expose them in screenshots or a demo.
- [ ] Handle a bad/empty input and an unavailable or failed AI request honestly; do not show fabricated success.
- [ ] Test the main flow with realistic inputs, capture screenshots as the project evolves, and keep a short known-issues list.
- [ ] Freeze new features early enough to rehearse and submit.

### Devpost — due by 4:30 PM per the slide

- [ ] Project name and track.
- [ ] Short description of the problem, who it is for, and what was built.
- [ ] Snowflake features and AI used.
- [ ] Screenshots or a short demo video.
- [ ] Honest “How Baked Is It?” self-score and a note on what is real versus mocked.
- [ ] Complete the quick post-event survey if required.
- [ ] Confirm the submission is saved and accessible before the deadline.

### Demo readiness

- [ ] Open with the user problem and value in one sentence.
- [ ] Demonstrate the complete workflow on the challenge data.
- [ ] Make the Snowflake features and meaningful AI contribution visible.
- [ ] Show one checked result and how the user can act on it.
- [ ] State limitations and the honest maturity score.
- [ ] Rehearse within the organizer's allotted presentation time.
- [ ] Prepare a fallback (screenshots or a short video) in case Wi-Fi, account access, or a live AI call fails.

## Current project status and guidance for the next AI

- The workspace has the supplied JPEG slide photos in this folder; it does not currently have a PowerPoint file or application source code.
- No Snowflake account connection or application integration has been made.
- Do not invent a project idea, claim an integration is working, or create a starter app until the user supplies the intended problem/project details and confirms the desired stack.
- When implementation is requested, inspect the actual project first, use its existing conventions, ask which track/problem is selected if not already stated, and implement only against the provided Snowflake account and permitted data.
- Keep credentials in local environment configuration; never write secrets into source files, this document, or screenshots.

## Image index

These filenames are the retained representative images. The WhatsApp-named copies that showed identical slide photos were removed; `WhatsApp Image 2026-10-16 at 12.49.04 (12).jpeg` is retained because it is the only photo of the CoCo workshop slide.

| Image | Visible slide/topic |
|---|---|
| [A.jpeg](./A.jpeg) | Data you can use; includes the warning against confidential, regulated, or personal employer data. |
| [B.jpeg](./B.jpeg) | Three project essentials: visual component, intentional Snowflake features, and AI doing real work. |
| [C.jpeg](./C.jpeg) | Track-specific judging criteria and weights. |
| [D.jpeg](./D.jpeg) | “How Baked Is It?” five-level maturity scale. |
| [E.jpeg](./E.jpeg) | Devpost checklist and 4:30 PM submission deadline. |
| [F.jpeg](./F.jpeg) | Prizes for the three tracks. |
| [G.jpeg](./G.jpeg) | Team, code, Snowflake-account, timing, and conduct rules. |
| [H.jpeg](./H.jpeg) | Hack the Experience track. |
| [HACK_EXP.jpeg](./HACK_EXP.jpeg) | Pro tips. |
| [HACK_GRIND.jpeg](./HACK_GRIND.jpeg) | Hack the Grind track. |
| [HACK_QUESTION.jpeg](./HACK_QUESTION.jpeg) | Track-selection decision flow. |
| [TRACK.jpeg](./TRACK.jpeg) | Hack the Question track. |
| [CoCo workshop photo](<./WhatsApp Image 2026-10-16 at 12.49.04 (12).jpeg>) | “Zero to Shipped with CoCo” workshop schedule and format. |
