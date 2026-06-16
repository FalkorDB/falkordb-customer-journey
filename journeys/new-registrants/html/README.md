# New Registrants email HTML

HubSpot ready coded email templates for the 3 step new registrants flow. The wording source of truth is the [folder README](../README.md). These files are the visual layout.

| File | Step | Subject |
|---|---|---|
| [`day1-welcome.html`](day1-welcome.html) | Day 1 | Welcome to FalkorDB. Start your free trial. |
| [`day3-use-cases.html`](day3-use-cases.html) | Day 3 | See what teams build on FalkorDB |
| [`day6-best-practices.html`](day6-best-practices.html) | Day 6 | A few best practices for building on FalkorDB |

The reusable header, footer, and body skeleton is in [`../../templates/base-template-hubspot.html`](../../templates/base-template-hubspot.html).

## HubSpot notes

- Each file is a coded email template. In HubSpot, use Design Manager, create a coded Email file, and paste the contents.
- Required HubL tokens are already included: `standard_header_includes`, `standard_footer_includes`, `site_settings.company_name` and address, `unsubscribe_link`, `view_as_page_url`, and a `content_attribute "email_body"` region. See [`../../hubspot-coded-email-guide.md`](../../hubspot-coded-email-guide.md).
- Icons are referenced from icons8 by URL. For production, upload the brand tinted PNGs to the HubSpot File Manager and swap the `src` values. The PNG sources are kept locally, not in this repo.
- The subject line is set in the HubSpot email settings, not in the HTML.
