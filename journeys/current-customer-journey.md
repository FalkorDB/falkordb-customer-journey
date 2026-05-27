# Current Customer Journey (As-Is)

This file documents the current HubSpot registration / pending-registration sequence as it exists today.

**Source of truth:** [HubSpot registration journey](https://app-eu1.hubspot.com/sequences/144055056/sequence/248070596/edit?page=2)

**Audience:** contacts registered in HubSpot and pending registration.

**Status:** active.

---

## Sequence steps documented so far

| Step | Timing | HubSpot action | Audience / label | A/B test | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Day 1 | Automated Email | Registrants - First email | Yes | A | Documented |

---

## Step 1 — Automated Email - Day 1

**HubSpot label:** Registrants - First email

**A/B test:** Yes

**Version documented:** Version A

**Subject:** Welcome to FalkorDB! Let's Get You Started

### Email body

Hi {First Name},

Welcome to FalkorDB! We're excited to have you join our community! FalkorDB is here to help you manage and analyze your graph data with ease and efficiency.

Here's how to get started:

1. **Log in:** Visit <https://app.falkordb.cloud/signin> and use your credentials to access your dashboard.
2. **Explore our resources:** Check out our documentation to get familiar with FalkorDB capabilities.
3. **Graph RAG:** GraphRAG SDK is here to support you with building a multi-tenant and multi-agent RAG application.

If you have any questions, feel free to reach out by replying to this email or using the following channels:

- **Email:** support@falkordb.com
- **Discord:** <https://discord.gg/AEHAVvH5GU>
- **Forum:** <https://github.com/orgs/FalkorDB/discussions>

We are interested to learn more about your use case. Will be glad to chat: 30 min meeting.

Thanks,

The FalkorDB Team

---

## Notes / gaps to capture

- Version B of the A/B test is not documented yet.
- The exact HubSpot personalization token for the greeting should be confirmed.
- The "30 min meeting" link / CTA target should be captured if it exists in HubSpot.
- Remaining sequence steps after Day 1 still need to be documented.
