"""Build the bilingual (Arabic / English) devil's-advocate audit of the homepage prototype.

Writes research/audit/homepage-audit.html and prints it to research/homepage-audit-ar-en.pdf
with headless Chromium. Run: python3 research/audit/build_audit.py
"""
import html
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
OUT_HTML = HERE / "homepage-audit.html"
OUT_PDF = HERE.parent / "homepage-audit-ar-en.pdf"
DATE_AR, DATE_EN = "21 أكتوبر 2026", "21 October 2026"
URL = "https://sanad-redesign.vercel.app"

SEV = {
    "C": ("حرج", "Critical", "#b3262d"),
    "H": ("مرتفع", "High", "#c9502a"),
    "M": ("متوسط", "Medium", "#8a5a00"),
    "L": ("منخفض", "Low", "#1a7f80"),
}

# Each finding: id, severity, area (ar, en), title (ar, en), finding (ar, en), why (ar, en),
# evidence (ar, en), fix (ar, en), owner (ar, en)
FINDINGS = [
    ("C1", "C", ("التبرع والدفع", "Giving and payment"),
     ("وسائل الدفع والوعود في النموذج أكبر مما تقدمه سند فعليًا",
      "The form promises payment options Sanad doesn't offer today"),
     ("يعرض النموذج Apple Pay وGoogle Pay وميزة والمحافظ الإلكترونية (فودافون كاش، اتصالات كاش، أورنج موني، WE Pay) وإنستاباي وفوري، وأربع عملات، وتبرعًا شهريًا تلقائيًا. (أزلنا وعد الإيصال وذكر واتساب، انظر قائمة ما أصلحناه.)",
      "The form shows Apple Pay, Google Pay, Meeza, mobile wallets (Vodafone Cash, Etisalat Cash, Orange Money, WE Pay), InstaPay and Fawry, four currencies and automatic monthly giving. (We removed the receipt promise and the WhatsApp mentions; see the fixed list.)"),
     ("صفحة التبرع الحالية لدى سند تقبل البطاقات فقط عبر بوابة البنك التجاري الدولي (Mastercard Hosted Checkout)، ولا تذكر أي إيصال. إذا رأى العميل وعودًا لا يستطيع الوفاء بها فسيفقد الثقة في التصميم كله، وإذا أُطلقت كما هي فسيشعر المتبرع بالخداع عند الدفع.",
      "Sanad's live donate page takes cards only, through CIB's Mastercard hosted checkout, and promises no receipt. If the client sees promises it can't keep, it will doubt the whole design; if it launches as is, donors will feel misled at checkout."),
     ("sanadorphans.org/donate/ ؛ شريط الثقة وخطوة الدفع في النموذج (الملحق، الصورة 5).",
      "sanadorphans.org/donate/; the prototype's trust strip and payment step (appendix, image 5)."),
     ("نسأل سند عن خطة بوابة الدفع، ونعرض فقط الوسائل المتاحة يوم الإطلاق، ونعرض الباقي كخطة مستقبلية في عرض التسليم لا في الواجهة.",
      "Ask Sanad for its gateway plan, show only the methods live on launch day, and present the rest as a roadmap in the handover deck rather than in the interface."),
     ("سند + الوكالة", "Sanad + agency")),
    ("C2", "C", ("المصداقية والصور", "Credibility and imagery"),
     ("صور مولّدة بالذكاء الاصطناعي لأطفال ومستفيدين بلا أي إشارة",
      "AI-generated photos of children and beneficiaries carry no label"),
     ("تسع صور مولّدة (أربع في البطل، أربع في «من نقوّي»، وصورة التحدي) تُظهر أطفالًا ومقدمي رعاية وأسرًا مصريين غير حقيقيين، وأُزيلت عبارة «صورة تعبيرية» بناءً على طلب المراجعة.",
      "Nine generated images (four in the hero, four in \"Who we strengthen\" and the challenge photo) show Egyptian children, caregivers and families who don't exist. The «صورة تعبيرية» labels were removed at review."),
     ("سند تبيع استشارات في سياسات حماية الطفل، وليس لديها سياسة منشورة للصور أو الموافقات. أي صحفي أو متبرع يكتشف أن «أطفال سند» مولّدون قد يتهم الجمعية بالتضليل، وهذا يمس جوهر مصداقيتها.",
      "Sanad sells child-safeguarding policy consulting and publishes no photo or consent policy. A journalist or donor who discovers that \"Sanad's children\" are synthetic could accuse the organisation of misleading the public, which goes to the heart of its credibility."),
     ("site/assets/hero و site/assets/photos ؛ لا توجد صفحة سياسة صور على sanadorphans.org.",
      "site/assets/hero and site/assets/photos; sanadorphans.org has no photo or consent policy page."),
     ("قبل الإرسال: موافقة مكتوبة من سند على استخدامها، أو إعادة عبارة «صورة تعبيرية»، والأفضل استبدالها بصور حقيقية بموافقة أصحابها قبل الإطلاق.",
      "Before sending: written approval from Sanad, or restore the «صورة تعبيرية» label. Best: replace them with real, consented photos before launch."),
     ("سند", "Sanad")),
    ("C3", "C", ("الرسالة", "Message"),
     ("جملة التموضع الأساسية ليست بكلمات سند، وموقعها يناقضها جزئيًا",
      "The core positioning line isn't Sanad's wording, and its own site partly contradicts it"),
     ("في البطل: «سند لا تدير دور رعاية، بل تقف خلف من يرعون الأطفال»، وفي قسم «من نقوّي»: «لا ندير دور رعاية. نحن نقوّي كل من يحيط بالطفل». موقع سند لا يقول هذا في أي صفحة. عنوانه الرئيسي هو رؤيته «عالم يستطيع فيه كل يتيم تشكيل مستقبله».",
      "The hero says «سند لا تدير دور رعاية، بل تقف خلف من يرعون الأطفال» and \"Who we strengthen\" says «لا ندير دور رعاية. نحن نقوّي كل من يحيط بالطفل». Sanad's site never says this; its homepage headline is its vision, «عالم يستطيع فيه كل يتيم تشكيل مستقبله»."),
     ("موقع سند يصف عملًا مباشرًا أيضًا: منح دراسية ومعدات لخريجي الرعاية (رانيا)، وبرامج فرصة ومبادر للشباب، وإرشاد الأسر الكافلة قبل الكفالة وبعدها، وصفحة التبرع تقول إن التبرع «يموّل برامج تصل مباشرة إلى الأطفال والشباب». قد ترى إدارة سند أن الرسالة تُنقص من عملها المباشر.",
      "Sanad's site also describes direct work: scholarships and equipment grants for care leavers (Raniah), the Forsa and Mobader youth programmes, and kafala counselling before and after placement. Its donate page says gifts fund «برامج تصل مباشرة إلى الأطفال والشباب». Sanad's leadership may feel the line undersells its direct work."),
     ("sanadorphans.org/ar/about ، /ar/donate ، /success-stories/raniah ، /services/kafala-family-support",
      "sanadorphans.org/ar/about, /ar/donate, /success-stories/raniah, /services/kafala-family-support"),
     ("نعرض الجملة على سند للاعتماد، أو نلطفها إلى «نقوّي المنظومة المحيطة بكل طفل»، ونضيف رؤية سند كسطر داعم في البطل.",
      "Put the line to Sanad for approval, or soften it to \"we strengthen the whole system around every child\", and add Sanad's vision as a supporting line in the hero."),
     ("سند + الوكالة", "Sanad + agency")),
    ("C4", "C", ("التبرع", "Giving"),
     ("حذف الزكاة قرار داخلي يعاكس الهدف الأول للعميل",
      "Dropping Zakat was an internal call that works against the client's first goal"),
     ("حذفنا اختيار صدقة/زكاة وحاسبة الزكاة وزر الزكاة في الشريط المتحرك، وكل ذكر للزكاة، بتوجيه «بدون أي توجه ديني». هذا التوجيه لم يأتِ من سند.",
      "We removed the Sadaqah/Zakat choice, the Zakat calculator, the mobile Zakat button and every mention of Zakat, following a \"no religious direction\" instruction. That instruction didn't come from Sanad."),
     ("صفحة سند الرئيسية وصفحة التبرع تقولان صراحة «زكاتك أو صدقتك أو تبرعك العام يموّل برامج…». موسم الزكاة ورمضان من أهم مواسم التبرع الفردي في مصر، والعميل طلب «تعظيم التبرعات الفردية». إذا اعترضت سند فسنبدو كمن غيّر استراتيجية جمع التبرعات دون إذن.",
      "Sanad's homepage and donate page say outright «زكاتك أو صدقتك أو تبرعك العام يموّل برامج…». Zakat and Ramadan are among the most important individual-giving seasons in Egypt, and the brief asks to \"maximise individual donations\". If Sanad objects, we'll look as if we changed its fundraising strategy without asking."),
     ("sanadorphans.org/ar/ ، /ar/donate/", "sanadorphans.org/ar/, /ar/donate/"),
     ("نعرضه على سند كقرار مفتوح مع البديلين. الحل الأخف: جملة محايدة «تقبل سند أموال الزكاة» دون حاسبة.",
      "Present it to Sanad as an open decision with both options. A lighter middle path: one neutral line, \"Sanad accepts Zakat\", without the calculator."),
     ("سند", "Sanad")),
    ("H1", "H", ("التحويل", "Conversion"),
     ("على الشاشات الكبيرة لا يظهر نموذج التبرع عند فتح الصفحة",
      "On desktop the donation form isn't visible when the page opens"),
     ("في نسخة البطل الحالية يظهر النموذج بعد التمرير بنحو شاشة كاملة، داخل التسلسل المثبّت. قبل ذلك كان النموذج ظاهرًا في الشاشة الأولى.",
      "In the current hero the form appears only after about one full screen of scrolling, inside the pinned sequence. Before, it was visible in the first screen."),
     ("هذا يناقض مبدأ في بحثنا نفسه: «النموذج في الشاشة الأولى». الزائر الذي لا يمرّر لا يرى مبلغًا ولا نموذجًا، بل زر «تبرّع الآن» فقط. قد يجذب التسلسل الانتباه، لكنه يضيف خطوة قبل التبرع.",
      "It contradicts a principle in our own research: \"the form in the first screen\". A visitor who doesn't scroll sees no amount and no form, only the \"Donate now\" button. The sequence may win attention, but it adds a step before giving."),
     ("الملحق، الصور 1 و2 و3 ؛ research/donation-ux-research.html", "Appendix, images 1, 2 and 3; research/donation-ux-research.html"),
     ("نتفق مع العميل على قياس التحويل (اختبار A/B بين البطل المثبّت ونسخة يظهر فيها النموذج فورًا)، أو نضيف اختيار المبلغ مختصرًا في البطل.",
      "Agree with the client to measure it: an A/B test between the pinned hero and a version with the form visible at once. Or add a compact amount picker to the hero."),
     ("الوكالة", "Agency")),
    ("H2", "H", ("التبرع", "Giving"),
     ("وصف المبالغ يناقض الرسالة ولا يتغير مع الغرض",
      "Amount captions contradict the message and don't change with the purpose"),
     ("150 ج.م «مستلزمات دراسية» و500 «دعم نفسي» خدمات مباشرة للطفل، بينما الرسالة تقول إن سند تقوّي من يرعاه. والأوصاف نفسها تظهر مع كل غرض، فمن يختار «تدريب مقدمي الرعاية» يرى 150 = مستلزمات دراسية.",
      "EGP 150 for «مستلزمات دراسية» and 500 for «دعم نفسي» are direct services to a child, while the message says Sanad strengthens those who care for children. The same captions appear for every purpose, so choosing «تدريب مقدمي الرعاية» still shows 150 = school supplies."),
     ("الأوصاف موروثة من موقع سند كما هي، لكن تصميمنا يبرز التناقض. ولا يوجد أي أساس تكلفة يثبت أن المبلغ يشتري ما يُذكر.",
      "The captions come straight from Sanad's site, but our design makes the contradiction more visible. Nothing shows that each amount actually buys what it says."),
     ("sanadorphans.org/ar/ (عنصر التبرع) ؛ النموذج في النموذج الأولي", "sanadorphans.org/ar/ (donation widget); the prototype's form"),
     ("نطلب من سند ثلاثة أمثلة أثر لكل غرض مبنية على تكلفة البرامج، ونجعل الأوصاف تتغير مع الغرض.",
      "Ask Sanad for three impact examples per purpose, based on programme costs, and make the captions change with the purpose."),
     ("سند", "Sanad")),
    ("H3", "H", ("الأرقام", "Figures"),
     ("صفحتنا صارت متسقة، لكن صفحات سند نفسها ما زالت متعارضة",
      "Our page is now consistent, but Sanad's own pages still disagree"),
     ("صفحات سند تتعارض: 20 محافظة (الرئيسية والخدمات) مقابل 19 (صفحة الفريق والملف التعريفي)، و18 عامًا مقابل 16 (قصص النجاح) و15 (التقرير 2022–2023)، والملف التعريفي ما زال يذكر 265 دارًا و4,440 طفلًا. أصلحنا صفحتنا: صارت تقول «منذ 2008» وعام التأسيس بدل عدد السنوات، وتعتمد 20 محافظة كما في عدادات سند الحالية.",
      "Sanad's pages disagree: 20 governorates (homepage and services) vs 19 (team page and portfolio); 18 years vs 16 (success stories) and 15 (2022–23 report); and the portfolio still shows 265 homes and 4,440 children. We fixed our page: it now says \"since 2008\" and shows the founding year instead of a count of years, and uses 20 governorates as on Sanad's current homepage counters."),
     ("صفحتنا لم تعد تناقض نفسها، لكن المتبرع الذي يفتح صفحة فريق سند أو ملفها التعريفي سيجد 19 محافظة وأرقامًا أقدم.",
      "Our page no longer contradicts itself, but a donor who opens Sanad's team page or portfolio will still find 19 governorates and older figures."),
     ("/ar/sanad-team ، /success-stories ، /ar/annual-reports ، sanad-portfolio.pdf", "/ar/sanad-team, /success-stories, /ar/annual-reports, sanad-portfolio.pdf"),
     ("أن تحدّث سند صفحة الفريق والملف التعريفي، وتعتمد ورقة أرقام واحدة بتاريخ «حتى …».",
      "Sanad updates its team page and portfolio, and approves one figures sheet with an \"as of\" date."),
     ("سند", "Sanad")),
    ("H5", "H", ("الهوية البصرية", "Visual identity"),
     ("ابتعاد عن الهوية البصرية لسند، وهو شرط صريح في طلب العميل",
      "Drift from Sanad's visual identity, an explicit requirement in the brief"),
     ("ألوان شعار سند: فيروزي #1EC0CA وأصفر #FFDA00. استخدمنا فيروزيًا قريبًا (#36C0CA) لكن كهرماني #F2B025 بدل الأصفر، وأضفنا المرجاني #C9502A للتبرع والكحلي. الخطوط أربع عائلات (Cairo وIBM Plex Sans Arabic وRoboto وAref Ruqaa). المركب مأخوذ من ملصقات حملة «رحلة تكمل رحلة» لا من الهوية الأساسية. والشعار المستخدم مكتوب عليه «Sanad for Orphans»، وموقع سند لا يستخدم هذا الاسم ويكتب «Sanad for Alternative Parental Care».",
      "Sanad's logo colours are teal #1EC0CA and yellow #FFDA00. We use a close teal (#36C0CA) but amber #F2B025 instead of the yellow, and added coral #C9502A for giving, plus navy. There are four font families (Cairo, IBM Plex Sans Arabic, Roboto, Aref Ruqaa). The boat comes from the \"رحلة تكمل رحلة\" story-poster campaign, not the core identity. The logo file reads \"Sanad for Orphans\", a name Sanad's site never uses; it writes \"Sanad for Alternative Parental Care\"."),
     ("الطلب نصًا: «أن يتوافق مع الهوية البصرية الخاصة بالجمعية». هذا أسهل اعتراض يمكن أن يقدمه فريق التسويق في سند.",
      "The brief says it must «يتوافق مع الهوية البصرية الخاصة بالجمعية». This is the easiest objection for Sanad's marketing team to raise."),
     ("sanad-slogn-off.svg ؛ متغيرات الألوان في site/index.html", "sanad-slogn-off.svg; colour variables in site/index.html"),
     ("نطلب دليل الهوية، ونستبدل الكهرماني بالأصفر الرسمي، ونقدّم المرجاني كلون وظيفي للتبرع للموافقة، ونقلّص الخطوط إلى عائلتين، ونؤكد نسخة الشعار.",
      "Ask for the brand guidelines, switch amber to the official yellow, present coral as a functional donate colour for approval, cut the fonts to two families and confirm the logo lockup."),
     ("الوكالة + سند", "Agency + Sanad")),
    ("H6", "H", ("القانون والثقة", "Legal and trust"),
     ("نجمع بيانات شخصية بلا سياسة خصوصية",
      "We collect personal data with no privacy policy"),
     ("النموذج يطلب الاسم، ورقم الموبايل والبريد اختياريًا. لا توجد صفحات سياسات نربط بها: موقع سند نفسه بلا سياسة خصوصية أو استرداد (/privacy-policy تعطي 404)، فأزلنا روابطها المؤقتة من التذييل.",
      "The form asks for a name, and optionally a mobile number and email. There are no policy pages to link to: Sanad's own site has no privacy or refund policy (/privacy-policy returns 404), so we removed the placeholder policy links from the footer."),
     ("قانون حماية البيانات الشخصية المصري (رقم 151 لسنة 2020) يجعل هذا خطرًا قانونيًا، والمتبرع الحذر يبحث عن هذه الروابط قبل الدفع.",
      "Egypt's Personal Data Protection Law (No. 151 of 2020) makes this a legal risk, and careful donors look for these links before paying."),
     ("sanadorphans.org/privacy-policy (404)", "sanadorphans.org/privacy-policy (404)"),
     ("صياغة سياسة خصوصية وسياسة استرداد قبل الإطلاق.",
      "Draft a privacy policy and a refund policy before launch."),
     ("سند (قانوني)", "Sanad (legal)")),
    ("H8", "H", ("إمكانية الوصول", "Accessibility"),
     ("حركة بلا وسيلة إيقاف، ونموذج لا يصل إليه مستخدم لوحة المفاتيح بسهولة",
      "Motion with no way to stop it, and a form keyboard users can't easily reach"),
     ("بعد إزالة زر «أوقف الحركة» صار شريط الشعارات يتحرك بلا توقف ولا يتوقف إلا بمرور الفأرة. وفي البطل المثبّت يبقى النموذج غير قابل للتركيز حتى يُمرَّر إليه، فمن يتنقل بزر Tab من أزرار البطل يتخطاه.",
      "Since the pause button was removed, the logo strip moves endlessly and stops only on mouse hover. In the pinned hero the form can't take focus until it's scrolled into view, so someone tabbing from the hero buttons skips past it."),
     ("WCAG 2.2.2 تشترط وسيلة لإيقاف أي حركة تستمر أكثر من 5 ثوانٍ. وضع «تقليل الحركة» يعمل جيدًا، لكنه لا يغطي من لا يفعّله.",
      "WCAG 2.2.2 requires a way to pause anything that moves for more than 5 seconds. Reduced-motion mode works well, but it doesn't cover people who haven't turned it on."),
     ("فحص يدوي ؛ فحص axe-core آلي (0 مخالفات بعد الإصلاحات، لكنه لا يختبر هذين البندين)", "Manual check; automated axe-core scan (0 violations after fixes, but it doesn't test these two)"),
     ("إعادة وسيلة إيقاف صغيرة أو إيقاف الشريط بعد دورة واحدة، وإضافة رابط تخطٍّ «انتقل إلى التبرع» في أول الصفحة.",
      "Bring back a small pause control or stop the strip after one cycle, and add a \"Skip to donation\" link at the top of the page."),
     ("الوكالة", "Agency")),
    ("M1", "M", ("الثقة", "Trust"),
     ("أقوى إشارات الثقة لدى سند غائبة",
      "Sanad's strongest trust signals are missing"),
     ("ما يظهر هو Pearson فقط. غائب: أول شهادة مهنية معتمدة دوليًا في المنطقة العربية (2012)، ومعايير جودة الرعاية التي اعتمدتها وزارة التضامن (2014، مع PwC)، والجوائز (أيقونة نجاح المرأة المصرية 2022، جائزة PDF للتميز 2020، مصر الخير 2019، الأمير محمد بن فهد 2017)، والمؤسِّسة عزة عبد الحميد، وتاريخ «وطنية» منذ 2008.",
      "Only Pearson appears. Missing: the first internationally accredited professional certificate in the Arab region (2012), care quality standards adopted by the Ministry of Social Solidarity (2014, with PwC), the awards (Egyptian Woman Icon of Success 2022, PDF Award of Excellence 2020, Masr ElKhair 2019, Prince Mohammed bin Fahad 2017), founder Azza Abdel Hamid, and the Wataneya history since 2008."),
     ("المتبرع الجديد يحتاج سببًا للثقة قبل الدفع، وهذه أسباب موثقة نمتلكها ولا نعرضها.",
      "A new donor needs a reason to trust before paying, and these are documented reasons we have but don't show."),
     ("/ar/awards ، /ar/achievements ، /ar/board-members", "/ar/awards, /ar/achievements, /ar/board-members"),
     ("شريط اعتمادات وجوائز مختصر قرب النموذج.", "A compact credentials and awards strip near the form."),
     ("الوكالة", "Agency")),
    ("M2", "M", ("الشفافية", "Transparency"),
     ("لا شيء يجيب عن «أين يذهب تبرعي؟»",
      "Nothing answers \"where does my money go?\""),
     ("حذفنا لوحة الشفافية لأنها كانت فارغة، وسند لا تنشر قوائم مالية؛ تقاريرها السنوية فنية فقط.",
      "We removed the transparency panel because it was empty, and Sanad publishes no financial statements; its annual reports are technical only."),
     ("المتبرع الشهري تحديدًا يسأل هذا السؤال، وغيابه نقطة ضعف أمام المنافسين.",
      "Monthly donors in particular ask this, and its absence is a weak spot against competitors."),
     ("/ar/annual-reports", "/ar/annual-reports"),
     ("أن تنشر سند ملخصًا ماليًا مدققًا، ونضيف كتلة «كيف نستخدم تبرعك» عند توفره.",
      "Sanad publishes an audited financial summary, and we add a \"How we use your gift\" block once it exists."),
     ("سند", "Sanad")),
    ("M3", "M", ("التحويل", "Conversion"),
     ("اختيارات افتراضية قد تبدو ضاغطة",
      "Default choices that may feel pushy"),
     ("«شهريًا» محدد مسبقًا بشارة «الأثر الأكبر» بلا دليل، و«أتحمّل رسوم الدفع» مُفعّلة مسبقًا.",
      "\"Monthly\" is preselected with an unproven \"Most impact\" badge, and \"I'll cover the payment fee\" is pre-ticked."),
     ("الإضافات المفعّلة مسبقًا تُعد نمطًا مظلمًا في أدلة جمع التبرعات الأخلاقية، وقد تزيد التراجع عند الدفع.",
      "Pre-ticked add-ons count as a dark pattern in ethical fundraising guidance, and they can increase drop-off at checkout."),
     ("النموذج، الخطوتان 1 و2", "The form, steps 1 and 2"),
     ("إبقاء «شهريًا» افتراضيًا مع جملة تشرح السبب، وجعل خيار الرسوم غير مفعّل افتراضيًا.",
      "Keep monthly as the default with a line explaining why, and leave the fee option unticked by default."),
     ("الوكالة", "Agency")),
    ("M4", "M", ("المحتوى", "Content"),
     ("القصص لا تقول من هم أصحابها",
      "The stories don't say who their people are"),
     ("رانيا ووجيه وسحر وعلاء كلهم خريجو رعاية، وسحر تعمل اليوم في سند كمنسقة تطوير دور الأيتام. الصفحة لا تذكر ذلك، و«كل القصص» لا يقود إلى صفحات سند العشر.",
      "Raniah, Wageeh, Sahar and Alaa are all care leavers, and Sahar now works at Sanad as a coordinator in orphanage development. The page doesn't say so, and \"All stories\" doesn't lead to Sanad's ten story pages."),
     ("«من خريجة رعاية إلى منسقة في سند» أقوى دليل أثر لدينا، وهو غير مستخدم.",
      "\"From care leaver to coordinator at Sanad\" is the strongest proof of impact we have, and it's unused."),
     ("/success-stories/{raniah,wageeh,sahar,alaa}", "/success-stories/{raniah,wageeh,sahar,alaa}"),
     ("سطر تعريفي لكل قصة، وربطها بصفحاتها الكاملة.", "Add one line per story on who the person is, and link to the full story pages."),
     ("الوكالة", "Agency")),
    ("M5", "M", ("الجوال", "Mobile"),
     ("نموذج التبرع بعيد على الجوال",
      "The donation form sits far down on mobile"),
     ("على عرض 390px يأتي النموذج بعد النص ثم تكوين الصور، على بعد نحو 1,500px، ويعتمد الوصول إليه على شريط «تبرع الآن» الثابت.",
      "At 390px the form comes after the copy and then the photo composition, about 1,500px down. Reaching it depends on the sticky \"Donate now\" bar."),
     ("معظم زيارات المواقع المصرية من الجوال، فالمسافة إلى النموذج تؤثر مباشرة على التحويل.",
      "Most visits to Egyptian sites come from phones, so the distance to the form directly affects conversion."),
     ("الملحق، الصورة 4", "Appendix, image 4"),
     ("اختبار وضع النموذج قبل تكوين الصور على الجوال.", "Test placing the form before the photo composition on mobile."),
     ("الوكالة", "Agency")),
    ("M6", "M", ("الأداء", "Performance"),
     ("ميزانية الحركة والخطوط ثقيلة لأجهزة متوسطة",
      "The motion and font budget is heavy for mid-range phones"),
     ("بطل مثبّت ودخولات لكل قسم وحركات مستمرة. الخطوط 254 كيلوبايت، أي نحو 40% من وزن الصفحة (634 كيلوبايت على سطح المكتب، 665 على الجوال).",
      "A pinned hero, an entrance for every section and continuous motion. Fonts weigh 254 KB, about 40% of the page (634 KB on desktop, 665 KB on mobile)."),
     ("أجهزة أندرويد المتوسطة شائعة في مصر، والحركة الزائدة قد تبدو «استعراضية» لجمعية خيرية.",
      "Mid-range Android phones are common in Egypt, and too much motion can look showy for a charity."),
     ("قياس الشبكة في بيئة الاختبار ؛ الملحق «نتائج الفحص»", "Network measurement in the test environment; appendix \"Test results\""),
     ("تحديد ميزانية أداء، والاختبار على جهاز أندرويد متوسط حقيقي، وتقليص الخطوط.",
      "Set a performance budget, test on a real mid-range Android phone and cut the fonts down."),
     ("الوكالة", "Agency")),
    ("M7", "M", ("الثقة", "Trust"),
     ("ادعاء الشراكات أقوى من الدليل",
      "The partnership claim is stronger than the evidence"),
     ("العنوان «تثق بنا الحكومة ووكالات الأمم المتحدة وكبرى الشركات» مع 69 شعارًا. نحو 30 شعارًا لم نستطع تحديد أصحابها، وصفحة الشركاء لدى سند فارغة.",
      "The headline says \"Trusted by government, UN agencies and leading companies\" over 69 logos. We couldn't identify about 30 of them, and Sanad's partners page is empty."),
     ("ادعاء «ثقة وكالات الأمم المتحدة» يحتاج إذنًا وتأكيدًا من كل جهة.",
      "Claiming \"UN agencies trust us\" needs permission and confirmation from each one."),
     ("/ar/partners-network (فارغة)", "/ar/partners-network (empty)"),
     ("تخفيف العنوان إلى «شركاء الأثر»، والحصول على قائمة الشركاء وأذونات الشعارات.",
      "Soften the headline to \"Impact partners\", and get the partner list and logo permissions."),
     ("سند", "Sanad")),
    ("M8", "M", ("التنقل", "Navigation"),
     ("روابط لا تقود إلى أي مكان",
      "Links that lead nowhere"),
     ("القائمة الرئيسية والتذييل صارا نسخة من قائمة سند وتذييلها بروابطهما الحقيقية. ما زالت مؤقتة: «اعرف أكثر» في بطاقات المحاور، و«كل القصص»، و«كل الأخبار» وبطاقات الأخبار، وأزرار قسم المؤسسات التي تقود إلى القسم نفسه.",
      "The main menu and the footer now mirror Sanad's, with their real links. Still placeholders: \"Learn more\" on the pillar cards, \"All stories\", \"All news\" and the news cards, and the organisations section's buttons, which lead back to that same section."),
     ("العميل سيضغط كل رابط في العرض.", "The client will click every link in the demo."),
     ("النموذج الأولي", "The prototype"),
     ("خريطة روابط كاملة إلى صفحات سند الحقيقية قبل الإرسال.", "Map every link to Sanad's real pages before sending."),
     ("الوكالة", "Agency")),
    ("L1", "L", ("الدقة", "Accuracy"),
     ("«1.4 مليون يتيم» بلا «نحو»", "\"1.4 million orphans\" without \"about\""),
     ("سند تكتب «حوالي مليون يتيم» وتبدّل بين «يتيم» و«طفل بلا رعاية والدية».",
      "Sanad writes «حوالي» (about) and switches between \"orphan\" and \"child without parental care\"."),
     ("فرق صغير، لكنه يظهر أمام خبراء الرعاية في سند.", "A small difference, but Sanad's care experts will spot it."),
     ("sanadorphans.org/ar/ (قسم التحدي)", "sanadorphans.org/ar/ (challenge section)"),
     ("«نحو 1.4 مليون طفل بلا رعاية والدية في مصر».", "\"About 1.4 million children without parental care in Egypt\"."),
     ("الوكالة", "Agency")),
    ("L2", "L", ("التقنية", "Technical"),
     ("اللغتان على عنوان واحد، والصفحة مستبعدة من محركات البحث",
      "Both languages share one URL, and the page is excluded from search engines"),
     ("التبديل بين العربية والإنجليزية يتم بجافاسكربت على عنوان واحد، بلا /ar/ و/en/ ولا hreflang. والوسم noindex موضوع عمدًا للنموذج.",
      "Switching between Arabic and English happens in JavaScript on one URL, with no /ar/ and /en/ and no hreflang. The noindex tag is there on purpose for the prototype."),
     ("مقبول للنموذج، خطر عند الإطلاق.", "Fine for a prototype, a risk at launch."),
     ("site/index.html", "site/index.html"),
     ("عنوانان منفصلان مع hreflang في التنفيذ، وإزالة noindex.", "Separate URLs with hreflang in the build, and remove noindex."),
     ("الوكالة", "Agency")),
    ("L3", "L", ("المحتوى", "Content"),
     ("ترجمة الفيلم إنجليزية", "The film's subtitles are in English"),
     ("فيلم «يعني إيه سند؟» عليه ترجمة إنجليزية محروقة في الصورة، والجمهور الأساسي عربي.",
      "The film «يعني إيه سند؟» has English subtitles burned into the picture, while the main audience is Arabic-speaking."),
     ("تفصيل يلاحظه العميل فورًا.", "A detail the client will notice at once."),
     ("youtube.com/watch?v=lNpo7sIex6s", "youtube.com/watch?v=lNpo7sIex6s"),
     ("طلب نسخة بدون ترجمة أو بترجمة عربية.", "Ask for a version with no subtitles or with Arabic subtitles."),
     ("سند", "Sanad")),
    ("L4", "L", ("المحتوى", "Content"),
     ("نشرة بريدية بلا نشرة", "A newsletter sign-up with no newsletter"),
     ("التذييل يدعو للاشتراك في «نشرة سند»، وصفحة النشرات لدى سند فارغة، والنموذج غير مربوط بأي نظام.",
      "The footer invites sign-ups to Sanad's newsletter, but Sanad's newsletters page is empty and the form isn't connected to anything."),
     ("وعد صغير غير منفّذ.", "A small promise that isn't kept."),
     ("/newsletters (فارغة)", "/newsletters (empty)"),
     ("إخفاؤه حتى توجد نشرة فعلًا.", "Hide it until a newsletter exists."),
     ("سند + الوكالة", "Sanad + agency")),
]

FIXED = [
    ("(M8 جزئيًا) التذييل صار بأعمدة تذييل سند ونصوصها: من نحن (عن سند، مجلس الإدارة، فريق العمل، الشركاء، تكريم جهود سند)، وخدماتنا (الخدمات الثماني)، ومعلومات التواصل بروابط اتصال وبريد، وكلها تقود إلى صفحات سند بلغة الصفحة. وصححنا العنوان إلى «بجوار قصر البارون» كما عند سند.",
     "(M8, in part) The footer now has Sanad's own footer columns and wording: Who We Are (About, Board Members, Sanad Team, Partners, Awards), Our Services (all eight) and Contact Information with tap-to-call and email links, all leading to Sanad's pages in the page's language. The Arabic address now says «بجوار قصر البارون» (next to Baron Palace), as Sanad's does."),
    ("(H7) القائمة الرئيسية أصبحت قائمة سند كما هي بالعربية والإنجليزية: من نحن، برامج الأثر، الخدمات الاستشارية (الخدمات الثماني)، الأثر، مركز المعرفة، المركز الإعلامي، شارك معنا، بقوائمها الفرعية وروابطها إلى صفحات سند. وزر «اطلب استشارة» يفتح نموذج طلب الاستشارة الفعلي لدى سند.",
     "(H7) The main menu is now Sanad's own menu, in Arabic and English: Who We Are, Impact Programs, Consulting Services (all eight services), Our Impact, Knowledge Hub, Media Center and Get Involved, with their submenus and links to Sanad's pages. \"Request a Consultation\" opens Sanad's real consultation form."),
    ("(C1) لم يذكر موقع سند أي إيصال، فأزلنا كل وعود الإيصال وذكر واتساب: سطر «إيصال فوري على واتساب» في شريط الثقة وتحت زر التبرع، وسطر الإيصال في صفحة الشكر، وتلميحات الإيصال في الخانات، وبطاقة «حوّلت بالفعل؟»، وزر واتساب العائم. (أبقينا «(واتساب)» بجانب رقم الموبايل في التذييل، فهو رقم سند الفعلي.) صار رقم الموبايل اختياريًا، وحلّ رقم الإشهار محل الإيصال في شريط الثقة.",
     "(C1) Sanad's site never mentions a receipt, so we removed every receipt promise and the WhatsApp mentions. That covers the \"instant WhatsApp receipt\" line in the trust strip and under the donate button, the receipt line on the thank-you step, the receipt hints in the fields, the \"Already transferred?\" card, and the floating WhatsApp button. (\"(WhatsApp)\" stays beside the mobile number in the footer, since it is Sanad's real number.) The mobile number is now optional, and the registration number replaces the receipt in the trust strip."),
    ("(H4) وصفنا رقم 1,921 بأنه «منظمة مجتمع مدني»، والأرجح أنه أفراد كما في ملف سند التعريفي. أصبح «كادرًا في المجتمع المدني»، مثل «كادرًا بوزارة التضامن» بجانبه، بانتظار تأكيد سند.",
     "(H4) We described 1,921 as \"civil society organisations\"; it's most likely people, as in Sanad's portfolio. It now reads \"civil society staff\", like the ministry-staff figure beside it, pending Sanad's confirmation."),
    ("(H3) «18 عامًا» صارت «منذ 2008» وعام التأسيس في البطل وشريط الثقة ولوحة الأثر وقسم القصص، فلا تتعارض مع أي صفحة لسند. وثبّتنا 20 محافظة كما في عدادات سند الحالية.",
     "(H3) \"18 years\" became \"since 2008\" and the founding year in the hero, trust strip, impact panel and stories section, so it can't conflict with any Sanad page. We kept 20 governorates, as on Sanad's current counters."),
    ("لون نص زر «تبرّع الآن» في التذييل كان رماديًا على المرجاني (تباين 3.0:1). أصبح أبيض.",
     "The footer's \"Donate now\" button had grey text on coral (contrast 3.0:1). It's white now."),
    ("لوحات القصص كانت <article role=\"tabpanel\"> وهو غير مسموح. أصبحت عناصر div.",
     "Story panels were <article role=\"tabpanel\">, which isn't allowed. They're divs now."),
    ("زر واتساب العائم كان خارج أي منطقة معلّمة. أُزيل الزر لاحقًا.",
     "The floating WhatsApp button sat outside any landmark. The button was later removed."),
    ("بعد الانتقال إلى الخطوة الثانية كان النموذج يتوقف جزئيًا تحت الشريط العلوي. يتوقف الآن تحته مباشرة.",
     "After moving to step 2, the form stopped partly under the header. It now lands just below it."),
    ("تأثير الارتفاع عند المرور فوق بطاقات «من نقوّي» والأخبار كان معطلًا بسبب أنماط الظهور. يعمل الآن.",
     "The hover lift on the \"Who we strengthen\" and news cards was overridden by the reveal styles. It works again."),
]

STRENGTHS = [
    ("مسار تبرع واضح بخطوتين، بالأغراض الأربعة ذاتها التي يستخدمها موقع سند.",
     "A clear two-step giving flow, with the same four purposes Sanad's site uses."),
    ("كل أرقام التحدي بمصادرها كما يذكرها موقع سند (اليونيسف 2014، SOS 2023، وزارة التضامن 2023).",
     "Every challenge figure carries its source as Sanad's site gives it (UNICEF 2014, SOS 2023, MoSS 2023)."),
    ("القصص الأربع حقيقية من موقع سند، والدعوة «ساعد في كتابة القصة القادمة» تموّل تمكين الشباب، وهو ما ينطبق على أصحابها.",
     "The four stories are real ones from Sanad's site, and the call \"Help write the next story\" funds youth empowerment, which fits who they are."),
    ("المحاور الثلاثة وبرامجها الخمسة منقولة من موقع سند بنصها.", "The three pillars and their five programmes are taken from Sanad's site word for word."),
    ("الحسابات البنكية الثلاثة بأرقامها الصحيحة مع زر نسخ.", "All three bank accounts with the correct numbers and a copy button."),
    ("عربية أولًا مع نسخة إنجليزية كاملة، وتعمل على كل العروض، ووضع «تقليل الحركة» يعرض كل شيء ثابتًا.",
     "Arabic first with a full English version, working at every width, and reduced-motion mode shows everything still."),
    ("فحص axe-core الآلي: صفر مخالفات على سطح المكتب والجوال بعد الإصلاحات.",
     "Automated axe-core scan: zero violations on desktop and mobile after the fixes."),
]

SCORE = [
    ("تعظيم التبرعات الفردية", "Maximise individual donations", "partial",
     ("مسار التبرع قوي، لكن C1 وC4 وH1 وH2 قد تخفض التحويل أو تقوّض الثقة.",
      "The giving flow is strong, but C1, C4, H1 and H2 could lower conversion or undermine trust.")),
    ("تشجيع المتصفحين على التبرع وفق التوجهات الاستراتيجية الحالية", "Encourage visitors to give, in line with Sanad's current strategy", "partial",
     ("أهداف سند 2024–2030: الكفالة ومنع الارتداد، والرعاية اللاحقة، وقدرات الجمعيات، وكوادر جديدة. أغراض التبرع لا تعكسها مباشرة، أما الاستشارات فصارت في القائمة وزر الاستشارة.",
      "Sanad's 2024–2030 goals are kafala and preventing relapse, aftercare, the capacity of associations and new qualified staff. The giving purposes don't map onto them directly; consulting now has its menu and button.")),
    ("تصميم عصري وجذاب وسهل التصفح والاستخدام", "A modern, attractive design that is easy to browse and use", "met",
     ("مُحقق مع ملاحظات: الحركة (H8، M6) وموضع النموذج على الجوال (M5).",
      "Met, with caveats: motion (H8, M6) and the form's position on mobile (M5).")),
    ("التوافق مع الهوية البصرية للجمعية", "Consistent with Sanad's visual identity", "risk",
     ("في خطر: الألوان والخطوط واسم الشعار (H5).", "At risk: colours, fonts and the name on the logo (H5).")),
]

QUESTIONS = [
    ("هل تريد سند إبراز الزكاة في الموقع؟ (C4)", "Does Sanad want Zakat featured on the site? (C4)"),
    ("ما وسائل الدفع المتاحة يوم الإطلاق؟ (C1)", "Which payment methods will be live on launch day? (C1)"),
    ("هل يمكن إرسال إيصال تبرع، وبأي وسيلة؟ أزلنا الوعد حتى تؤكد سند. (C1)", "Can Sanad send donation receipts, and how? We removed the promise until Sanad confirms. (C1)"),
    ("هل توافق سند على الصور المولّدة؟ وهل لديها صور حقيقية بموافقات؟ (C2)", "Does Sanad approve the generated photos? Does it have real, consented photos? (C2)"),
    ("هل تعتمد سند جملة «سند لا تدير دور رعاية…»؟ (C3)", "Does Sanad approve the line «سند لا تدير دور رعاية…»? (C3)"),
    ("ورقة أرقام واحدة معتمدة بتاريخ، مع تأكيد أن 1,921 أفراد لا منظمات. (H3)", "One approved, dated figures sheet, confirming that 1,921 counts people, not organisations. (H3)"),
    ("أمثلة أثر لكل غرض تبرع مبنية على التكلفة. (H2)", "Cost-based impact examples for each giving purpose. (H2)"),
    ("دليل الهوية البصرية ونسخة الشعار المعتمدة. (H5)", "The brand guidelines and the approved logo lockup. (H5)"),
    ("سياسة الخصوصية وسياسة الاسترداد. (H6)", "A privacy policy and a refund policy. (H6)"),
    ("قائمة الشركاء وأذونات استخدام الشعارات. (M7)", "The partner list and permission to use the logos. (M7)"),
]

SHOTS = [
    ("../../../tmp/shots/d-t5000.jpg", "البطل على سطح المكتب بعد انتهاء الحركة الافتتاحية", "Desktop hero after the intro"),
    ("../../../tmp/shots/d-p0.45.jpg", "منتصف التمرير: الصور تدور بعيدًا والنموذج يتفتح من المركز", "Mid-scroll: the photos swirl away and the form opens from the centre"),
    ("../../../tmp/shots/d-p0.8.jpg", "النموذج مكتمل الظهور داخل البطل المثبّت", "The form fully open inside the pinned hero"),
    ("../../../tmp/shots/m-t5000.jpg", "الجوال (390px): النص أولًا ثم الصور", "Mobile (390px): copy first, then the photos"),
    ("../../../tmp/shots/step2.jpg", "الخطوة 2: وسائل الدفع المعروضة", "Step 2: the payment methods shown"),
]

TESTS = [
    ("فحص axe-core 4.10 على الموقع المنشور قبل الإصلاحات: مخالفة خطيرة واحدة (تباين)، وأخرى متوسطة (منطقة معلّمة)، وثالثة بسيطة (دور ARIA).",
     "axe-core 4.10 on the live site before the fixes: one serious violation (contrast), one moderate (landmark) and one minor (ARIA role)."),
    ("بعد الإصلاحات: صفر مخالفات على 1280px و390px.", "After the fixes: zero violations at 1280px and 390px."),
    ("وزن الصفحة المنشورة: 634 كيلوبايت على سطح المكتب (51 طلبًا)، و665 كيلوبايت على الجوال. منها: الصور 330–361، والخطوط 254، والمستند 45 كيلوبايت.",
     "Live page weight: 634 KB on desktop (51 requests) and 665 KB on mobile. Of that, images are 330–361 KB, fonts 254 KB and the document 45 KB."),
    ("اختبارات وظيفية آلية بالعربية والإنجليزية على 1280px و390px: النموذج بخطواته الثلاث، وروابط التبرع، والفيلم، والقصص، وتبديل اللغة، ووضع «تقليل الحركة». كلها ناجحة بلا أخطاء في وحدة التحكم.",
     "Automated functional tests in Arabic and English at 1280px and 390px covered all three form steps, the donate links, the film, the stories, the language switch and reduced-motion mode. All passed with no console errors."),
    ("القياسات من بيئة اختبار سحابية وليست بديلًا عن اختبار جهاز حقيقي.", "Measurements come from a cloud test environment and don't replace testing on a real device."),
]

SOURCES = [
    "sanadorphans.org/ar/about/", "sanadorphans.org/about/", "sanadorphans.org/ar/ (الرئيسية / home)", "sanadorphans.org/ar/donate/",
    "sanadorphans.org/ar/services/ + 8 service pages", "sanadorphans.org/ar/awards/", "sanadorphans.org/ar/achievements/",
    "sanadorphans.org/ar/board-members/", "sanadorphans.org/ar/sanad-team/", "sanadorphans.org/success-stories/ + 4 stories",
    "sanadorphans.org/ar/prevention/, /ar/protection/, /ar/advocacy/ + 5 programmes", "sanadorphans.org/ar/annual-reports/",
    "sanadorphans.org/ar/our-aspirations/", "sanadorphans.org/ar/news/, /ar/press-releases/", "sanad-portfolio.pdf (60 pp.)",
    "research/donation-ux-research.html (بحثنا السابق / our earlier research)",
]

T = {
    "ar": dict(
        part="الجزء الأول: العربية", title="تدقيق تجربة المستخدم والواجهة للصفحة الرئيسية",
        sub="قراءة نقدية من موقع «محامي الشيطان» قبل إرسال التصميم إلى سند",
        summary="الملخص التنفيذي",
        summary_p=("التصميم قوي بصريًا ومسار التبرع واضح، لكنه في صورته الحالية يحمل مخاطر قد تجعل سند تعترض عليه أو تفقد الثقة فيه. أخطر ما فيه أربع نقاط حرجة: وعود دفع أكبر من قدرات سند، وصور مولّدة لأطفال بلا إشارة، وجملة تموضع ليست بكلمات سند، وحذف الزكاة دون موافقتها. لا نوصي بإرسال التصميم قبل حسم النقاط الحرجة أو عرضها على سند صراحة كقرارات مفتوحة."),
        counts="عدد الملاحظات", top="قبل الإرسال، يجب حسم:",
        method="المنهج والمصادر",
        method_p=("راجعنا النموذج المنشور على سطح المكتب (1280px و1366×657) والجوال (390px)، بالعربية والإنجليزية وفي وضع «تقليل الحركة». شغّلنا فحص axe-core الآلي لإمكانية الوصول، وقسنا وزن الصفحة، وأعدنا الاختبارات الوظيفية. ثم قارنّا كل ادعاء وكل رقم في الصفحة بطلب العميل وبصفحة «من نحن» وبكامل محتوى موقع سند، وبحثنا السابق. تبنّينا عمدًا موقف من يبحث عن الأخطاء: كل ملاحظة هي ما قد يقوله فريق سند أو متبرع متشكك."),
        brief="طلب العميل", brief_q="«تعظيم التبرعات الفردية وجعل تصميم الموقع يتناسب مع تشجيع المتصفحين على التبرع وفقا للتوجهات الاستراتيجية الحالية لدى الجمعية. كذلك أن يكون التصميم عصري وجذاب وسهل التصفح والاستخدام وأن يتوافق مع الهوية البصرية الخاصة بجمعية سند.»",
        score="مطابقة طلب العميل", req="المتطلب", verdict="الحكم", note="الملاحظة",
        v={"met": "مُحقق", "partial": "جزئيًا", "risk": "في خطر"},
        findings="الملاحظات حسب الخطورة", area="المجال", f_found="ما وجدناه", f_why="لماذا يهم", f_ev="الدليل", f_fix="التوصية", f_owner="المسؤول",
        fixed="أصلحناه أثناء التدقيق", strengths="ما يعمل جيدًا", questions="قرارات مطلوبة من سند",
        appendix="ملحق: صور ونتائج الفحص", tests="نتائج الفحص", sources="المصادر",
        prepared=f"إعداد فريق التصميم · {DATE_AR} · النموذج: {URL}",
    ),
    "en": dict(
        part="Part 2: English", title="Homepage UI/UX audit",
        sub="A devil's-advocate review before the design goes to Sanad",
        summary="Executive summary",
        summary_p=("The design is visually strong and the giving flow is clear, but as it stands it carries risks that could lead Sanad to reject it or lose trust in it. The four critical points are: payment promises beyond what Sanad offers, generated photos of children with no label, a positioning line that isn't Sanad's wording, and dropping Zakat without Sanad's agreement. We don't recommend sending the design until the critical points are resolved or put to Sanad explicitly as open decisions."),
        counts="Findings", top="Must be settled before sending:",
        method="Method and sources",
        method_p=("We reviewed the live prototype on desktop (1280px and 1366×657) and mobile (390px), in Arabic and English and with reduced motion. We ran an automated axe-core accessibility scan, measured page weight and re-ran the functional tests. Then we checked every claim and figure on the page against the client's brief, Sanad's About page, the whole of Sanad's website and our earlier research. We deliberately took the stance of someone looking for faults: each finding is what Sanad's team or a sceptical donor might say."),
        brief="The client's brief", brief_q="Maximise individual donations, and design the site to encourage visitors to give in line with the association's current strategic directions. The design should also be modern, attractive and easy to browse and use, and consistent with Sanad's visual identity. (Translated from the Arabic brief.)",
        score="Scorecard against the brief", req="Requirement", verdict="Verdict", note="Note",
        v={"met": "Met", "partial": "Partly met", "risk": "At risk"},
        findings="Findings by severity", area="Area", f_found="What we found", f_why="Why it matters", f_ev="Evidence", f_fix="Recommendation", f_owner="Owner",
        fixed="Fixed during the audit", strengths="What's working", questions="Decisions needed from Sanad",
        appendix="Appendix: screenshots and test results", tests="Test results", sources="Sources",
        prepared=f"Prepared by the design team · {DATE_EN} · Prototype: {URL}",
    ),
}


def e(s):
    return html.escape(s, quote=False)


def part(lang):
    t = T[lang]
    i = 0 if lang == "ar" else 1
    d = "rtl" if lang == "ar" else "ltr"
    counts = {k: sum(1 for f in FINDINGS if f[1] == k) for k in SEV}
    crit = [f for f in FINDINGS if f[1] == "C"]
    out = [f'<section class="part" dir="{d}" lang="{lang}">']
    out.append(f'<div class="part-head"><span class="kicker">{e(t["part"])}</span><h1>{e(t["title"])}</h1><p class="sub">{e(t["sub"])}</p><p class="prep">{e(t["prepared"])}</p></div>')
    # summary
    out.append(f'<h2>{e(t["summary"])}</h2><p>{e(t["summary_p"])}</p>')
    out.append('<div class="counts">' + "".join(
        f'<div class="count" style="--c:{SEV[k][2]}"><b>{counts[k]}</b><span>{e(SEV[k][i])}</span></div>' for k in SEV) +
        f'<div class="count fixed"><b>{len(FIXED)}</b><span>{e(t["fixed"])}</span></div></div>')
    out.append(f'<p class="top"><b>{e(t["top"])}</b></p><ol class="toplist">' + "".join(f'<li><span class="id">{f[0]}</span> {e(f[3][i])}</li>' for f in crit) + "</ol>")
    # method + brief
    out.append(f'<h2>{e(t["method"])}</h2><p>{e(t["method_p"])}</p>')
    out.append(f'<div class="brief"><b>{e(t["brief"])}</b><p>{e(t["brief_q"])}</p></div>')
    # scorecard
    out.append(f'<h2>{e(t["score"])}</h2><table class="score"><thead><tr><th>{e(t["req"])}</th><th>{e(t["verdict"])}</th><th>{e(t["note"])}</th></tr></thead><tbody>')
    for ar, en, v, note in SCORE:
        out.append(f'<tr><td>{e(ar if lang == "ar" else en)}</td><td><span class="v v-{v}">{e(t["v"][v])}</span></td><td>{e(note[i])}</td></tr>')
    out.append("</tbody></table>")
    # findings
    out.append(f'<h2>{e(t["findings"])}</h2>')
    for fid, sev, area, title, found, why, ev, fix, owner in FINDINGS:
        out.append(f'<article class="finding" style="--c:{SEV[sev][2]}"><header><span class="id">{fid}</span><span class="sev">{e(SEV[sev][i])}</span><span class="area">{e(area[i])}</span></header>'
                   f'<h3>{e(title[i])}</h3><dl>'
                   f'<dt>{e(t["f_found"])}</dt><dd>{e(found[i])}</dd>'
                   f'<dt>{e(t["f_why"])}</dt><dd>{e(why[i])}</dd>'
                   f'<dt>{e(t["f_ev"])}</dt><dd class="ev">{e(ev[i])}</dd>'
                   f'<dt>{e(t["f_fix"])}</dt><dd class="fix">{e(fix[i])}</dd>'
                   f'<dt>{e(t["f_owner"])}</dt><dd>{e(owner[i])}</dd></dl></article>')
    # fixed, strengths, questions
    out.append(f'<h2>{e(t["fixed"])}</h2><ul class="ticks">' + "".join(f"<li>{e(x[i])}</li>" for x in FIXED) + "</ul>")
    out.append(f'<h2>{e(t["strengths"])}</h2><ul class="ticks">' + "".join(f"<li>{e(x[i])}</li>" for x in STRENGTHS) + "</ul>")
    out.append(f'<h2>{e(t["questions"])}</h2><ol class="qs">' + "".join(f"<li>{e(x[i])}</li>" for x in QUESTIONS) + "</ol>")
    # appendix
    out.append(f'<h2 class="break">{e(t["appendix"])}</h2><div class="shots">')
    for n, (src, cap_ar, cap_en) in enumerate(SHOTS, 1):
        out.append(f'<figure class="{"tall" if "step2" in src or "m-t5000" in src else ""}"><img src="{src}" alt=""><figcaption><b>{n}</b> {e(cap_ar if lang == "ar" else cap_en)}</figcaption></figure>')
    out.append(f'</div><h3>{e(t["tests"])}</h3><ul>' + "".join(f"<li>{e(x[i])}</li>" for x in TESTS) + "</ul>")
    out.append(f'<h3>{e(t["sources"])}</h3><ul class="src" dir="ltr">' + "".join(f"<li>{e(s)}</li>" for s in SOURCES) + "</ul>")
    out.append("</section>")
    return "\n".join(out)


CSS = """
@page { size: A4; margin: 16mm 15mm 18mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: "Cairo", "IBM Plex Sans Arabic", system-ui, sans-serif; color: #0f2233; font-size: 10.2pt; line-height: 1.65; }
[lang="en"] { font-family: "IBM Plex Sans", "Cairo", system-ui, sans-serif; line-height: 1.55; }
h1, h2, h3 { font-family: "IBM Plex Sans Arabic", "IBM Plex Sans", sans-serif; line-height: 1.3; margin: 0; }
.cover { height: 260mm; display: flex; flex-direction: column; justify-content: space-between; padding: 6mm 2mm; page-break-after: always; }
.cover .brand { display: flex; align-items: center; gap: 10px; color: #1a7f80; font-weight: 800; letter-spacing: .02em; }
.cover .brand i { width: 14px; height: 14px; border-radius: 50%; background: #1ec0ca; box-shadow: 18px 0 0 #ffda00; margin-inline-end: 22px; }
.cover h1 { font-size: 27pt; margin-top: 6mm; }
.cover .en h1 { font-size: 23pt; }
.cover .ar, .cover .en { padding: 8mm 0; border-top: 2px solid #e3f5f6; }
.cover p { margin: 3mm 0 0; color: #4c5f6e; font-size: 12pt; }
.cover .meta { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; font-size: 9.5pt; color: #4c5f6e; border-top: 2px solid #0f2233; padding-top: 5mm; }
.cover .meta b { color: #0f2233; display: block; }
.cover .stamp { align-self: flex-start; background: #b3262d; color: #fff; font-weight: 800; padding: 2mm 5mm; border-radius: 3mm; font-size: 10pt; }
.part { page-break-before: always; }
.part-head { padding-bottom: 5mm; margin-bottom: 4mm; border-bottom: 3px solid #1ec0ca; }
.kicker { color: #1a7f80; font-weight: 800; font-size: 9pt; letter-spacing: .04em; }
.part-head h1 { font-size: 20pt; margin-top: 1mm; }
.sub { color: #4c5f6e; font-size: 11.5pt; margin: 1mm 0 0; }
.prep { color: #7a8b97; font-size: 8.5pt; margin: 2mm 0 0; }
h2 { font-size: 13.5pt; margin: 7mm 0 2.5mm; padding-inline-start: 3mm; border-inline-start: 4px solid #1ec0ca; break-after: avoid; page-break-after: avoid; }
table.score, .brief, .counts { break-inside: avoid; page-break-inside: avoid; }
h2.break { page-break-before: always; margin-top: 0; }
h3 { font-size: 11pt; margin: 5mm 0 2mm; }
p { margin: 0 0 2.5mm; }
.counts { display: grid; grid-template-columns: repeat(5, 1fr); gap: 3mm; margin: 4mm 0; }
.count { border: 1.5px solid var(--c); border-radius: 3mm; padding: 2.5mm 3mm; display: flex; flex-direction: column; }
.count b { font-size: 18pt; line-height: 1.1; color: var(--c); font-family: "IBM Plex Sans", sans-serif; }
.count span { font-size: 8.5pt; font-weight: 700; }
.count.fixed { --c: #17704a; }
.top { margin-top: 3mm; }
.toplist { margin: 0; padding-inline-start: 0; list-style: none; }
.toplist li { padding: 1.6mm 0; border-bottom: 1px dashed #d9e6e8; }
.id { display: inline-block; min-width: 9mm; font-family: "IBM Plex Sans", sans-serif; font-weight: 800; color: #b3262d; }
.brief { background: #f4efe6; border-radius: 3mm; padding: 3.5mm 4.5mm; margin: 3mm 0; }
.brief p { margin: 1mm 0 0; font-style: italic; }
table.score { width: 100%; border-collapse: collapse; font-size: 9.4pt; }
.score th { text-align: start; background: #0f2233; color: #fff; padding: 2mm 2.5mm; font-weight: 700; }
.score td { padding: 2.2mm 2.5mm; border-bottom: 1px solid #d9e6e8; vertical-align: top; }
.score td:first-child { font-weight: 700; width: 34%; }
.score td:nth-child(2) { width: 15%; }
.v { display: inline-block; border-radius: 99px; padding: .4mm 3mm; font-weight: 800; font-size: 8.5pt; white-space: nowrap; }
.v-met { background: #e2f4ec; color: #17704a; }
.v-partial { background: #fdf2d6; color: #8a5a00; }
.v-risk { background: #fbe3e1; color: #b3262d; }
.finding { border: 1px solid #d9e6e8; border-inline-start: 5px solid var(--c); border-radius: 2.5mm; padding: 2.4mm 3.5mm 1.6mm; margin: 0 0 3mm; page-break-inside: avoid; }
.finding header { display: flex; align-items: center; gap: 3mm; font-size: 8.6pt; }
.finding .id { color: var(--c); min-width: 0; font-size: 10pt; }
.sev { background: var(--c); color: #fff; border-radius: 99px; padding: .2mm 2.6mm; font-weight: 800; }
.area { color: #4c5f6e; font-weight: 700; }
.finding h3 { margin: 1mm 0 1.2mm; font-size: 10.6pt; }
dl { display: grid; grid-template-columns: 22mm 1fr; gap: .6mm 3mm; margin: 0; font-size: 9pt; line-height: 1.55; }
[lang="en"] dl { grid-template-columns: 31mm 1fr; line-height: 1.45; }
dt { font-weight: 800; color: #4c5f6e; }
dd { margin: 0; }
dd.ev { color: #4c5f6e; font-size: 8.4pt; overflow-wrap: anywhere; unicode-bidi: plaintext; }
dd.fix { font-weight: 600; color: #135f60; }
ul, ol { margin: 0 0 2mm; padding-inline-start: 6mm; }
li { margin-bottom: 1.2mm; }
.ticks { list-style: none; padding-inline-start: 0; }
.ticks li { padding-inline-start: 6mm; position: relative; }
.ticks li::before { content: "✓"; position: absolute; inset-inline-start: 0; color: #17704a; font-weight: 800; }
.qs li::marker { font-weight: 800; color: #1a7f80; }
.shots { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }
.shots figure { margin: 0; page-break-inside: avoid; }
.shots img { width: 100%; border: 1px solid #d9e6e8; border-radius: 2mm; display: block; }
.shots figure.tall img { max-height: 120mm; width: auto; max-width: 100%; margin-inline: auto; }
.shots figcaption { font-size: 8.5pt; color: #4c5f6e; margin-top: 1.5mm; }
.shots figcaption b { color: #1a7f80; }
.src { font-size: 8.3pt; color: #4c5f6e; columns: 2; }
"""


def build():
    # screenshots are copied next to the HTML so the PDF build is self-contained
    shots_dir = HERE / "shots"
    shots_dir.mkdir(exist_ok=True)
    doc = f"""<!doctype html><html lang="ar"><head><meta charset="utf-8"><title>Sanad homepage audit</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=IBM+Plex+Sans+Arabic:wght@600;700&family=IBM+Plex+Sans:wght@400;600;700;800&display=swap">
<style>{CSS}</style></head><body>
<section class="cover">
  <div class="brand"><i></i>SANAD · سند</div>
  <div>
    <div class="ar" dir="rtl" lang="ar"><h1>تدقيق تجربة المستخدم والواجهة للصفحة الرئيسية</h1><p>قراءة نقدية من موقع «محامي الشيطان» قبل إرسال التصميم إلى سند</p></div>
    <div class="en" dir="ltr" lang="en"><h1>Homepage UI/UX audit</h1><p>A devil's-advocate review before the design goes to Sanad</p></div>
  </div>
  <span class="stamp">مراجعة داخلية قبل التسليم · Internal pre-handover review</span>
  <div class="meta" dir="ltr"><div><b>Prototype · النموذج</b>{URL}</div><div><b>Date · التاريخ</b>{DATE_EN} · {DATE_AR}</div>
  <div><b>Contents · المحتوى</b>Part 1: Arabic · الجزء الأول: العربية<br>Part 2: English · الجزء الثاني: الإنجليزية</div><div><b>Findings · الملاحظات</b>{len(FINDINGS)} + {len(FIXED)} fixed · أُصلح</div></div>
</section>
{part("ar")}
{part("en")}
</body></html>"""
    doc = doc.replace("../../../tmp/shots/", "shots/")
    OUT_HTML.write_text(doc, encoding="utf-8")
    return OUT_HTML


if __name__ == "__main__":
    p = build()
    subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=15000", f"--print-to-pdf={OUT_PDF}", p.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("wrote", OUT_HTML.relative_to(HERE.parent.parent), "and", OUT_PDF.relative_to(HERE.parent.parent), OUT_PDF.stat().st_size // 1024, "KB")
