# Sanad redesign

Website redesign for Sanad for Alternative Parental Care (sanadorphans.org). The goal is to grow individual donations.

## Research

- `research/donation-ux-research.html` is the phase 1 UX audit and homepage blueprint. It covers annotated screenshots of the current homepage, donor proto-personas, design principles, an Arabic mobile-first wireframe, a donation flow, brand colour and contrast checks, a prioritised backlog, the measurement plan and the roadmap to Ramadan 2027.
- `research/donation-ux-research-ar.html` is the full Arabic (right-to-left) version of the same report, for the client.
- `research/assets/` holds section crops of the current English desktop homepage (October 2026) used in the audit.

Open the HTML file in a browser to read it.

## Homepage prototype

- `site/index.html` is the redesigned homepage, built from the research wireframe. It is Arabic first, with an English toggle (or `?lang=en`), uses Cairo for body text and IBM Plex Sans Arabic for headlines (with Roboto for any Latin letters and digits in them), and uses Sanad's brand palette, figures, stories and bank details from the current site.
- `site/dist/sanad-homepage-prototype.html` is the same page as one self-contained file for sharing. Rebuild it with `python3 site/build.py` after editing `index.html`.

The page is built around one idea: Sanad doesn't care for orphans directly, it strengthens the people who do («نكون سندًا لمن يكونون سندًا لهم»). It has no religious framing: gifts are monthly or one-time, with no Zakat or Sadaqah choice.

- **Hero**: the headline, Sanad's film «يعني إيه سند؟» and the donation form. The film's poster wipes in, slowly zooms, and plays in a dialog. Nothing loads from YouTube (youtube-nocookie.com) until the visitor presses play, and closing the dialog stops the film. This is the only place the film appears.
- **Donation form**: the same four purposes as the current site's form (تنمية الأطفال، تمكين الشباب، تدريب مقدمي الرعاية، تبرع عام). It also uses the current site's amounts and captions: 150 for school supplies, 500 for psychosocial support and 1,000 for caregiver training.
- **Trusted partners**: 69 partner logos from the current site, in colour, in two rows that drift in opposite directions. Hovering pauses them, and a button stops them for good.
- **The challenge**: 140 million children without parental care worldwide, 35 million in Africa and 1.4 million orphans in Egypt, with their sources. Each figure has a bar drawn to scale, set over a photo.
- **What we do**: the three pillars (prevention, protection, empowerment) with their programs, a "read more" panel and a give link for each.
- **Who we strengthen**: opens with Sanad's own "نهجنا: التغيير المنظومي" text, then shows the five groups Sanad works with. Each card gives the group, the pillar its program belongs to, a description drawn from Sanad's pillar texts and the program name from the current site. The cards carry no figures, because Sanad doesn't publish one for every group. All eight published figures appear in the impact panel under the cards.
- **Stories**: all four stories from the current site (Raniah, Wageeh, Sahar and Alaa), each with its Arabic or English poster, quote and hashtags. Visitors move between them with a picker or arrows.
- **Get involved**: four colour cards.
- **Bank transfer**: each bank card shows that bank's logo.

Cards share motifs taken from the current site: dot grids, wave bottoms, icon circles and colour bars. With reduced motion turned on, everything shows in its final state.

Sources for every piece of content: the text, figures, programs, stories, partner list, bank details and donation purposes all come from sanadorphans.org (Arabic and English homepage, October 2026). The one exception is "Pearson-accredited training", which comes from Sanad's impact page. The section headlines, the five-group framing of "Who we strengthen" and the short connecting lines are new copy.

Images:
- The logo, story posters, news photos and the caregivers' graduation photo are Sanad's originals from sanadorphans.org.
- The partner logos (`site/assets/partners/`) and bank logos (`site/assets/banks/`) come from sanadorphans.org.
- The film poster is the video's YouTube thumbnail, cropped above the burned-in subtitle.
- The photos in `site/assets/photos/` were generated with Magnific (Nano Banana 2). They cover the care home, kafala family, training workshop, young man at work and the challenge photo. They are not real beneficiaries, so each one carries a small «صورة تعبيرية» (illustrative image) label.

Working in the prototype: the two-step donation form (monthly or one-time, purpose, amount, payment method, validation, thank-you and monthly upsell), the film player, the story picker, copy buttons for bank accounts, the WhatsApp receipt link, the language switch and the sticky mobile donate bar. No payment details are collected and nothing is sent anywhere.

Before production:
- Add the IBAN / SWIFT numbers to the bank cards if Sanad wants them shown.
- Replace the generated photos with real Sanad photos (with consent) when they are available.
- Confirm the partner list and get each partner's logo approval. Some logos are named only in the file names, so add proper alt text for those.
- Confirm the landline number (+20 2 26907195) and the consent for each story.
- Point the in-page `#` links at the real pages and connect the form to the payment gateway.
- The payment logos in `site/assets/pay/` were supplied by the project team. Show only the methods the chosen gateway actually supports, and follow each provider's logo guidelines.
