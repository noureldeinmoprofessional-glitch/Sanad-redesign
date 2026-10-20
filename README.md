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

The page is built around one idea: Sanad doesn't care for orphans directly, it strengthens the people who do («نكون سندًا لمن يكونون سندًا لهم»). The hero shows this as a "circle of care": the child at the centre, then a trained caregiver, the care home or kafala family, Sanad, and the donor. The rings draw in sequence on load, dots of support flow inward to the child, and the amount chosen in the donation form lights up the ring it strengthens. Below the hero, the page brings back everything the current homepage carries, redesigned:

- **Trusted partners**: 69 partner logos from the current site in two rows that drift in opposite directions. They turn to full colour on hover, hovering pauses them, and a button stops them for good.
- **The challenge**: 140 million children without parental care worldwide, 35 million in Africa and 1.4 million orphans in Egypt, drawn as nested circles at true scale, with sources.
- **The film**: Sanad's film «يعني إيه سند؟». It opens from a chip in the hero, from the challenge section, or from a cinematic poster that grows into place as you scroll. It plays in a dialog. Nothing loads from YouTube (youtube-nocookie.com) until the visitor presses play, and closing the dialog stops the film.
- **What we do**: the three pillars (prevention, protection, empowerment) with their programs, a "read more" panel and a give link for each.
- **Who we strengthen**: introduces the five groups Sanad works with.
- **How your gift travels**: follows the brand's boat along a four-step route as you scroll. It ends with every impact figure from the current site.
- **Get involved**: four colour cards.
- **Bank transfer**: each bank card shows that bank's logo.

Cards share motifs taken from the current site: dot grids, wave bottoms, icon circles and colour bars. The rest of the page fades in gently. With reduced motion turned on, everything shows in its final state.

Images: the logo, story posters and photos are Sanad's own full-size originals from sanadorphans.org. The illustrations in `site/assets/art/` (the caregiver and child at the centre of the circle, the care home, the kafala family and the training session) were generated with Magnific (Nano Banana 2) in the style of Sanad's story posters. They are illustrations, not photos of real beneficiaries. The partner logos (`site/assets/partners/`), bank logos (`site/assets/banks/`) and the film poster (the video's YouTube thumbnail) come from sanadorphans.org and Sanad's YouTube channel.

Working in the prototype: the two-step donation form (monthly or one-time, Zakat / Sadaqah / General, fund, amount, payment method, validation, thank-you and monthly upsell), the zakat calculator, story tabs, copy buttons for bank accounts, the WhatsApp receipt link, the language switch and the sticky mobile donate bar. No payment details are collected and nothing is sent anywhere.

Before production:
- Fill the marked placeholders: the zakat Sharia statement, program and operations percentages, and the IBAN / SWIFT numbers.
- Confirm the partner list and get each partner's logo approval. Some logos are named only in the file names, so add proper alt text for those.
- Confirm the fund-to-amount labels, the campaign progress figures (currently examples), the landline number (+20 2 26907195) and the consent for each story.
- Point the in-page `#` links at the real pages and connect the form to the payment gateway.
- The payment logos in `site/assets/pay/` were supplied by the project team. Show only the methods the chosen gateway actually supports, and follow each provider's logo guidelines.
