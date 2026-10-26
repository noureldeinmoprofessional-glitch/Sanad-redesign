# Sanad redesign

Website redesign for Sanad for Alternative Parental Care (sanadorphans.org). The goal is to grow individual donations.

## Research

- `research/donation-ux-research.html` is the phase 1 UX audit and homepage blueprint. It covers annotated screenshots of the current homepage, donor proto-personas, design principles, an Arabic mobile-first wireframe, a donation flow, brand colour and contrast checks, a prioritised backlog, the measurement plan and the roadmap to Ramadan 2027.
- `research/donation-ux-research-ar.html` is the full Arabic (right-to-left) version of the same report, for the client.
- `research/assets/` holds section crops of the current English desktop homepage (October 2026) used in the audit.

- `research/homepage-audit-ar-en.pdf` is a bilingual (Arabic, then English) devil's-advocate audit of the homepage prototype. It checks the design against the client's brief, Sanad's About page and the rest of sanadorphans.org, an automated accessibility scan and page-weight measurements. It's an internal review to settle before handover, and it lists the decisions needed from Sanad. Rebuild it with `python3 research/audit/build_audit.py`; the source text is in that script and the screenshots are in `research/audit/shots/`.

Open the HTML file in a browser to read it.

## Homepage prototype

- `site/index.html` is the redesigned homepage, built from the research wireframe. It is Arabic first, with an English toggle (or `?lang=en`), uses Cairo for body text and IBM Plex Sans Arabic for headlines (with Roboto for any Latin letters and digits in them), and uses Sanad's brand palette, figures, stories and bank details from the current site.
- `site/dist/sanad-homepage-prototype.html` is the same page as one self-contained file for sharing. Rebuild it with `python3 site/build.py` after editing `index.html`.

The page is built around one idea: Sanad doesn't care for orphans directly, it strengthens the people who do («نكون سندًا لمن يكونون سندًا لهم»). It has no religious framing: gifts are monthly or one-time, with no Zakat or Sadaqah choice.

- **Hero**: the headline, two calls to action (donate, and «تعرّف على سند», which opens Sanad's film), three figures from Sanad's site, and a photo composition. The composition is a main photo with three smaller photos joined by a hand-drawn line («نؤهّل مقدّمي الرعاية»، «نمكّن الشباب»، «نرتقي بجودة الرعاية»), plus Sanad's vision («عالم يستطيع فيه كل يتيم تشكيل مستقبله») in a teal shape. On load, the main photo opens from the centre, the three photos spiral out of it into place, and the line draws through them; faint brand boats drift behind. On desktop the hero then holds still while you scroll. The photos swirl away along the spiral, the main photo collapses into its centre, and the donation form opens out of that point. After that the page carries on. Any donate link scrolls straight to the open form. Moving to the form's second step releases the hold, so the taller steps scroll normally. Phones show the copy, then the composition (which plays its intro when it comes into view), then the form. With reduced motion, desktop shows the copy and form side by side. The film opens in a dialog and loads nothing from YouTube (youtube-nocookie.com) until the visitor presses play.
- **Donation form**: the same four purposes as the current site's form (تنمية الأطفال، تمكين الشباب، تدريب مقدمي الرعاية، تبرع عام). It also uses the current site's amounts and captions: 150 for school supplies, 500 for psychosocial support and 1,000 for caregiver training.
- **Trusted partners**: 69 partner logos from the current site, in colour, in two rows that drift in opposite directions. Hovering pauses them.
- **The challenge**: 140 million children without parental care worldwide, 35 million in Africa and 1.4 million orphans in Egypt, with their sources. Each figure has a bar drawn to scale, set over a photo.
- **What we do**: the three pillars (prevention, protection, empowerment) with their programs, a "read more" panel and a give link for each.
- **Who we strengthen**: opens with Sanad's own "نهجنا: التغيير المنظومي" text, then shows the five groups Sanad works with. Each card gives the group, the pillar its program belongs to, a description drawn from Sanad's pillar texts and the program name from the current site. The cards carry no figures, because Sanad doesn't publish one for every group. All eight published figures appear in the impact panel under the cards.
- **Stories**: all four stories from the current site (Raniah, Wageeh, Sahar and Alaa), each with its Arabic or English poster, quote and hashtags. Visitors move between them with a picker or arrows.
- **Get involved**: four colour cards.
- **Bank transfer**: each bank card shows that bank's logo.

- **Header**: the nav, «اطلب استشارة» (request a consultation), the donate button and a compact language button (globe + EN / ع). Below 1100px the nav folds into the menu, and on phones the consultation link moves there too.

Cards share motifs taken from the current site: dot grids, wave bottoms, icon circles and colour bars. Each section has its own entrance:
- **Headlines:** a line draws beside the eyebrow and the words rise out of a mask.
- **Trust strip:** the icons pop in.
- **Partner logos:** the rows slide in from opposite sides.
- **Challenge:** the photo wipes open, with a slight parallax.
- **Pillars:** the cards tilt up into place.
- **Who we strengthen:** the photos rise like a curtain.
- **Impact panel:** it opens from its centre.
- **Stories:** the first poster slides in.
- **Bank cards:** they swing in, and a light sweeps across each logo.
- **Get-involved cards:** each colour spreads out from its icon.
- **News:** the photos wipe down.

With reduced motion turned on, everything shows in its final state.

Sources for every piece of content: the text, figures, programs, stories, partner list, bank details and donation purposes all come from sanadorphans.org (Arabic and English homepage, October 2026). The one exception is "Pearson-accredited training", which comes from Sanad's impact page. The section headlines, the five-group framing of "Who we strengthen" and the short connecting lines are new copy.

Images:
- The logo, story posters, news photos and the caregivers' graduation photo are Sanad's originals from sanadorphans.org.
- The partner logos (`site/assets/partners/`) and bank logos (`site/assets/banks/`) come from sanadorphans.org.
- The film poster is the video's YouTube thumbnail, cropped above the burned-in subtitle.
- The photos in `site/assets/photos/` and `site/assets/hero/` were generated with Magnific (Nano Banana 2), with no text in them. They cover the care home, kafala family, training workshop, young man at work, the challenge photo and the four hero photos. They are not real beneficiaries and, at the client's request, carry no «صورة تعبيرية» label.

Working in the prototype: the two-step donation form (monthly or one-time, purpose, amount, payment method, validation, thank-you and monthly upsell), the film player, the story picker, copy buttons for bank accounts, the language switch and the sticky mobile donate bar. No payment details are collected and nothing is sent anywhere.

Before production:
- Add the IBAN / SWIFT numbers to the bank cards if Sanad wants them shown.
- Replace the generated photos with real Sanad photos (with consent) before launch. They show people who are not Sanad's beneficiaries and are no longer labelled as illustrative.
- Confirm the partner list and get each partner's logo approval. Some logos are named only in the file names, so add proper alt text for those.
- Confirm with Sanad that 1,921 counts civil society staff (people), as the page now says, and ask it to align its team page (19 governorates) and portfolio PDF (older figures) with its homepage counters.
- Ask Sanad whether it can send donation receipts and how. The page makes no receipt promise and doesn't mention WhatsApp anywhere until that is confirmed.
- Confirm the landline number (+20 2 26907195) and the consent for each story.
- Point the in-page `#` links at the real pages and connect the form to the payment gateway.
- The payment logos in `site/assets/pay/` were supplied by the project team. Show only the methods the chosen gateway actually supports, and follow each provider's logo guidelines.
