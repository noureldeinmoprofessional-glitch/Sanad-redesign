# Sanad redesign

Website redesign for Sanad for Alternative Parental Care (sanadorphans.org). The goal is to grow individual donations.

## Research

- `research/donation-ux-research.html` is the phase 1 UX audit and homepage blueprint. It covers annotated screenshots of the current homepage, donor proto-personas, design principles, an Arabic mobile-first wireframe, a donation flow, brand colour and contrast checks, a prioritised backlog, the measurement plan and the roadmap to Ramadan 2027.
- `research/donation-ux-research-ar.html` is the full Arabic (right-to-left) version of the same report, for the client.
- `research/assets/` holds section crops of the current English desktop homepage (October 2026) used in the audit.

Open the HTML file in a browser to read it.

## Homepage prototype

- `site/index.html` is the redesigned homepage, built from the research wireframe. It is Arabic first, with an English toggle (or `?lang=en`), and uses Sanad's Cairo font, brand palette, figures, stories and bank details from the current site.
- `site/dist/sanad-homepage-prototype.html` is the same page as one self-contained file for sharing. Rebuild it with `python3 site/build.py` after editing `index.html`.

The page opens on Surah Al-Insan 76:8 in a bright theme. The verse stays in place while its words reveal one by one as the visitor scrolls, with the English translation (Sahih International) underneath and an amber highlight drawn across «وَيَتِيمًا» and "orphan". The paper boat from the story posters sails across as a progress marker. Once the verse is complete, the donation section rises over it as a sheet, its content coming in one item after another. If scrolling stops partway, the page finishes the rise, or returns to the verse when scrolling up. With reduced motion turned on, the verse and donation section show in full with no pinning or gliding.

Working in the prototype: the two-step donation form (monthly or one-time, Zakat / Sadaqah / General, fund, amount, payment method, validation, thank-you and monthly upsell), the zakat calculator, story tabs, copy buttons for bank accounts, the WhatsApp receipt link, the language switch and the sticky mobile donate bar. No payment details are collected and nothing is sent anywhere.

Before production:
- Replace the images in `site/assets/` with Sanad's originals. They were cropped from screenshots, so they are low resolution.
- Fill the marked placeholders: the zakat Sharia statement, program and operations percentages, and the IBAN / SWIFT numbers.
- Confirm the fund-to-amount labels, the campaign progress figures (currently examples), the landline number (+20 2 26907195) and the consent for each story.
- Point the in-page `#` links at the real pages and connect the form to the payment gateway.
