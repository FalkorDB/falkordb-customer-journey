# HubSpot HTML Marketing Email: format guide for future AI

A practical checklist for building a HubSpot marketing email as coded HTML. Written from real errors and warnings hit while building the FalkorDB journey emails. Follow this to produce a template that imports, validates, and sends without the back and forth.

---

## 1. Pick the right route first

There are two ways to get HTML into HubSpot. They behave very differently.

| Route | What it is | Images via `<img>` in HTML | Editing |
|---|---|---|---|
| **Coded email template (Design Manager)** | One full HTML file, type email. Recommended for a designed email. | Yes, `<img>` works | Marketers edit code or the email_body region |
| **Drag and drop email** | Built from modules on a canvas. The HTML you paste goes into an HTML module. | No. `<img>` in an HTML module breaks and causes alignment jumping and phantom drop zones. Use separate Image modules instead. | Drag and drop modules |

Rule of thumb: for a branded, table based design with icons, use a **coded email template**. Use drag and drop only when marketers need to rearrange blocks themselves, and then place images in Image modules, not in HTML.

---

## 2. Template annotation (top of the coded file)

Put this comment as the very first thing in the file so Design Manager treats it as an email template and lists it.

```html
<!--
  templateType: email
  isAvailableForNewContent: true
  label: My Email Name
-->
```

`isAvailableForNewContent: false` hides it from the picker when creating new emails. Use `true`.

---

## 3. Required HubL tokens (each missing one is a publish error)

These are not optional. HubSpot blocks sending until all are present. We hit each of these as a separate error.

| Token | Where it goes | Error if missing |
|---|---|---|
| `{{ standard_header_includes }}` | In `<head>`, just before `</head>` | "missing the required tag {{ standard_header_includes }}" |
| `{{ standard_footer_includes }}` | Just before `</body>` | "Template doesn't include the tag standard_footer_includes. Needed for HubSpot analytics" |
| `{{ site_settings.company_name }}` | Footer | "missing the required tag {{ site_settings.company_name }}" |
| `{{ unsubscribe_link }}` | Footer link href | CAN-SPAM, blocks send |
| `{{ view_as_page_url }}` | Footer link href | View in browser |

Physical mailing address (CAN-SPAM). Include the company address tokens in the footer too, or HubSpot flags a missing physical address:

```html
{{ site_settings.company_street_address_1 }}, {{ site_settings.company_city }}, {{ site_settings.company_state }} {{ site_settings.company_zip }} {{ site_settings.company_country }}
```

Minimal compliant footer:

```html
Copyright © 2026 {{ site_settings.company_name }}. All rights reserved.<br>
{{ site_settings.company_street_address_1 }}, {{ site_settings.company_city }}, {{ site_settings.company_state }} {{ site_settings.company_zip }} {{ site_settings.company_country }}<br><br>
<a href="{{ view_as_page_url }}">View in browser</a> &middot; <a href="{{ unsubscribe_link }}">Unsubscribe</a>
```

---

## 4. The email_body module (clears the blog/RSS warning)

Warning seen: "The template does not contain the module email_body, it will not work for blog/rss emails."

It is only a warning, not an error, and it does not matter for a normal automated or journey email. To clear it, wrap an editable body region in HubSpot's content_attribute, exactly as HubSpot's own default template does:

```html
{% content_attribute "email_body" %}
<p>Your editable body content here. This is the per send editable region.</p>
{% end_content_attribute %}
```

Include this once. Whatever you put between the tags is the default content and still renders.

---

## 5. Email safe HTML rules

Email clients strip most modern HTML and CSS. Stick to these.

- Layout with **tables**, not divs or flexbox or grid.
- **Inline CSS** on elements. A `<style>` block in the head is mostly ignored by Outlook and Gmail. Media queries must stay in a `<style>` block since they cannot be inlined.
- **Absolute URLs** for every image and link.
- **ALT text** on every image.
- No JavaScript. No external CSS or web fonts you depend on.
- Keep the body width around **600px**. Add a mobile media query for max-width 600.
- **Buttons**: use bulletproof buttons. An `<a>` styled as a button for modern clients, plus a VML `v:roundrect` fallback inside `<!--[if mso]>` for Outlook.
- **Preheader**: a hidden div at the top with the preview text.

Note: structural HTML comments like `<!--[if mso]>`, `<![endif]-->`, and `<!-- section -->` contain dashes by necessity. They are required and are not visible to recipients. Do not remove them.

---

## 6. Images and icons (the biggest gotcha)

What broke for us and how to avoid it:

1. **Do not hotlink URLs that contain raw `&`.** Example that fails: `https://img.icons8.com/?size=100&id=85066&format=png&color=7466FF`. Raw `&` is invalid in HTML, so HubSpot re parses and mangles the URL. The image then fails and you get random placeholder icons (a green plus, stray text). Fix by escaping each `&` as `&amp;`, or better, stop hotlinking.
2. **Best practice: upload images to the HubSpot File Manager** and reference the HubSpot hosted URL. Those URLs are clean, stable, and never mangled.
3. **In a drag and drop email, `<img>` in an HTML module does not render.** Use the Image module instead. In a coded template, `<img>` is fine.
4. Set explicit `width` and `height` on images and `style="display:block"` to avoid gaps.

---

## 7. Subject, title, preview

- The send **subject** is set in the HubSpot email settings, not in the HTML. The `<title>` tag does not control the subject.
- **Preview or preheader** text is the hidden div near the top of the body.

---

## 8. How to get the real rendered HTML back out of HubSpot

If you need to inspect what HubSpot produced, do not use the browser View Source on the editor page. That returns the editor app shell only (look for content-creator-ui and quartz-powered), and the email lives inside an iframe that View Source does not capture.

Instead:
- In the email editor, use **Actions, then Export** or copy the email HTML.
- Or send a test, open it in Gmail, then **Show original** and save that.
- Or in DevTools, find the email `<iframe>`, right click its `<html>` node, and Copy outerHTML.

---

## 9. Quick validation checklist before import

- [ ] Annotation block with `templateType: email`, `isAvailableForNewContent: true`.
- [ ] `{{ standard_header_includes }}` before `</head>`.
- [ ] `{{ standard_footer_includes }}` before `</body>`.
- [ ] `{{ site_settings.company_name }}` plus address tokens in the footer.
- [ ] `{{ unsubscribe_link }}` and `{{ view_as_page_url }}` in the footer.
- [ ] One `{% content_attribute "email_body" %} ... {% end_content_attribute %}` region.
- [ ] Tables for layout, inline CSS, media queries in a `<style>` block.
- [ ] All image and link URLs absolute. Image URLs have no raw `&`, or images are in File Manager.
- [ ] ALT text on images. Bulletproof buttons with VML fallback.
- [ ] Open and close tag counts balanced.

---

## 10. FalkorDB specifics (house style for these emails)

- Font: generic `sans-serif` for all journey emails. Not serif, not a named font.
- No dash punctuation in copy. No em or en dashes, no spaced dash separators. Rephrase into short sentences. Hyphens in compound words, code, and URLs are fine.
- Few commas. Short sentences.
- No first name greeting token.
- Brand colors: brand `#7466FF`, badge background `#EEEBFF`, body text `#374151`, heading `#191919`, page background `#F5F5F5`, divider `#E5E7EB`, muted footer `#6B7280`.
- Font sizes mapped to the HubSpot set: title 18, body 14, label 12, fine print 11. Avoid 36.
- See `email-style-guide.md` in this folder for the full token list, and `base-template-hubspot.html` for a reusable header, footer, and body skeleton.
