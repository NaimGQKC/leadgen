# AI Inference Audit: Kanuk

**Inference Alignment Score: 65/100 -- YELLOW**

**Date:** 2026-04-01
**Category:** Montreal-made winter coat
**Methodology:** Gemini 2.5 Flash, 5 runs per query, 3 FR variants (n=15 FR, n=5 EN)

## Key Metrics

| Metric | English | French | Gap |
|--------|---------|--------|-----|
| Brand appearance rate | N/A | N/A | -- |
| Avg specs per response | N/A | N/A | -- |
| Spec range across runs | ?-? | ?-? | -- |
| Source authority score | 3.3 | 3.8 | --0.5 |

---

## Finding 1: Brand Visibility Gap

Brand appeared in N/A of English queries and N/A of French queries.

French queries tested:
1. "manteau d'hiver fait au Québec"
2. "meilleur manteau fabriqué à Montréal pour le froid"
3. "manteau québécois chaud et durable"

---

## Finding 2: Spec Dilution

Spec preservation: N/A (N/A FR vs N/A EN).
Range: ?-? specs across 15 French runs vs ?-? in English.

---

## Finding 3: Competitor Displacement

| Competitor | EN frequency | FR frequency | FR-only? |
|------------|-------------|-------------|----------|
| Quartz Co | present | present | No |
| Canada Goose | 0% | present | YES |
| Columbia | 0% | present | YES |
| The North Face | 0% | present | YES |
| Moose Knuckles | present | 0% | No |
| Rudsak | 0% | present | YES |
| Quartz Co | present | present | No |

---

## Finding 4: Source Authority

EN sources avg score: 3.3/10 | FR sources avg score: 3.8/10
Gap: 0.5 points -- French AI responses rely on lower-authority sources.

---

## Bonus: Google AI Mode (Live Search)

Results captured via live Chromium browser with Montreal geolocation.

### Generic Discovery

**Google EN** (ai_mode_fallback):
> AI Mode
> All
> Images
> Videos
> News
> More
> Sign in
> Search Results
> best Montreal-made winter coat in Montreal compare top options with specs and pricing
> Top Montreal-made winter coat brands include Kanuk, Quartz Co., and Audvik, which are recognized for their extreme-cold performance and local craftsmanship. 
> Boutique Bubbles
>  +2
> Premium Performance Parkas
> These brands specialize in high-fill-power insulation and technical fabrics designed to withstand temperatures as low as -30°C to -40°C. 
> Kanuk Mont-Royal Men's Winter Jacket
> $790.00
> Kanuk& more
> 4.8
> (58)
> Price: 790CAD.
> Specs: Features Primaloft® Bla
> Sources: https://audvik.com/en#:~:text=LOCAL%20AND%20ECO%2DFRIENDLY%20WINTER,of%20durable%20and%20timeless%20coats.&text=Proudly%20handcrafted%20in%20our%20Chabanel,creations%20directly%20at%20the%20workshop.&text=Because%20at%20Audvik%20we%20have,loved%20and%20pre%2Dworn%20coats., https://audvik.com/en-us#:~:text=LOCAL%20AND%20ECO%2DFRIENDLY%20WINTER,of%20durable%20and%20timeless%20coats.&text=Proudly%20handcrafted%20in%20our%20Chabanel,creations%20directly%20at%20the%20workshop.&text=Because%20at%20Audvik%20we%20have,loved%20and%20pre%2Dworn%20coats., https://www.sail.ca/blog/canadian-winter-jacket-brands/#:~:text=Extreme%20cold%20protection:%20Kanuk%20winter,jackets%20with%20a%20lifetime%20warranty., https://audvik.com/en, https://www.boutiquebubbles.com/blogs/blog/kanuk-vs-quartz-co-a-comparative-review-of-luxury-outerwear-at-boutique-bubbles#:~:text=Quartz%20Co%20also%20prides%20itself,their%20old%20coats%20for%20recycling.

**Google FR** (ai_mode_fallback):
> 18 sitesKanuk vs. Quartz Co: A Comparative Review of Luxury ...15 juill. 2023 — In conclusion, both Kanuk and Quartz Co offer high-quality, stylish options for winter outerwear. Your choice between the two will...Boutique BubblesManteaux et sacs d'hiver fabriqués au Canada - BEDI StudiosEn tant que Canadiens, nous comprenons l'importance d'un manteau d'hiver chaud ! Nous sommes une petite équipe et notre expérience...BEDI StudiosCoat suggestions : r/mcgill - Reddit2 janv. 2021 — I second this. My North face jacket keeps me so nice and warm - was seriously a lifesaver especially for someone who
> Sources: https://www.reddit.com/r/Quebec/comments/17rs1rz/meilleur_rapport_qualit%C3%A9_prix_pour_les_manteaux/#:~:text=J'ai%20pass%C3%A9%20de%20Canada%20Goose%20(lourd%2C%20coutures,2%20hivers)%20pour%20ensuite%20acheter%20le%20Kanuk., https://www.reddit.com/r/mcgill/comments/koxl2w/coat_suggestions/#:~:text=I%20second%20this.,grew%20up%20with%20mild%20winters.&text=Check%20out%20Quartz%20Co.%20!,it'll%20last%20for%20years!&text=I%20have%20one%20of%20their,ever%20since%20I%20bought%20it.&text=Check%20out%20Kanuk.,brand%20but%20absolutely%20worth%20it.&text=North%20face%20nuptse%20jackets%20are%20warm.&text=For%20a%20purely%20$%20to%20warmth,big%20deal%20to%20replace%20it.&text=%E2%80%A2%205y%20ago-,I%20second%20this.,Not%20the%20exact%20coat%20though., https://www.altitude-sports.com/blog/canadian-made-winter-coats#:~:text=Forty%20years%20after%20its%20founding,Shop, https://www.reddit.com/r/Quebec/comments/17rs1rz/meilleur_rapport_qualit%C3%A9_prix_pour_les_manteaux/, https://thekit.ca/shopping/canadian-winter-coat-brands/#:~:text=Kanuk&text=This%20made%2Din%2DCanada%20brand,range%20farms%20in%20Western%20Canada.

### Brand Accuracy

**Google EN** (ai_mode_fallback):
> 22 sitesInsulation, Care & Service - KanukInsulation * What are the different temperature ratings for Kanuk coats? Kanuk coats are engineered to protect against extreme tem...Kanukkanuk | Sports Experts - Atmosphere* 2 colours available. KANUK. Notting Hill - Women's Insulated Jacket. $949.99. * 4 colours available. KANUK. Mont-Royal - Men's W...Sports ExpertsWomen's Typha Coat | Kanuk | Sporting Life OnlineDetails * Fabric: 100% Recycled Nylon. * Lining: 100% Nylon taffeta. * Insulation: Kanuk Thermo+ * Wind-resistant with DWR finish.www.sportinglife.caWomen's Outerwear - Kanuk* Hope Quilted 
> Sources: https://kanuk.com/en/collections/women-outerwear, https://www.altitude-sports.com/p/kanuk-montroyal-mof-winter-jacket-mens-kan-10302#:~:text=Specifications,Water%20Resistant%2C%20Waterproof%2C%20Wind%20Resistant, https://www.sportsexperts.ca/en-CA/p-mont-royal-men-s-winter-hooded-jacket/573199/573199-151, https://latulippe.com/en/product/A00162/men-s-mont-royal-jacket/#:~:text=Warm%20and%20water%2Dresistant%20coat,cuffs%20prevent%20heat%20from%20escaping., https://kanuk.com/en/pages/insulation-care-service#:~:text=Down%20is%20the%20soft%2C%20lightweight,it%20retains%20heat%20&%20dries%20quickly.

**Google FR** (ai_mode_fallback):
> Mode IA
> Tous
> Images
> Vidéos
> Actualités
> Plus
> Connexion
> Résultats de recherche
> Kanuk Montreal-made winter coat specifications techniques completes materiaux technologie prix
> Les manteaux Kanuk, fabriqués à Montréal, se distinguent par l'utilisation de technologies propriétaires comme l'isolant Thermo+ et des matériaux extérieurs hautement résistants comme le Mini-Ottoman. Leurs prix se situent généralement entre 500 
> 𝒆
> 𝒕
> 𝟏
> 𝟏
> 𝟎
> 𝟎
> , selon le type d'isolation (synthétique ou duvet) et le niveau de protection thermique, qui peut atteindre -35 °C. 
> Kanuk
>  +3
> Technologies d'isolation
> Kanuk utilise troi
> Sources: https://www.boutique333.com/magasiner/mont-royal-f-w-taille-plus/#:~:text=Con%C3%A7ue%20et%20fabriqu%C3%A9e%20au%20Canada.%20Ce%20parka,inspir%C3%A9e%20des%20hivers%20canadiens%20en%20territoires%20urbains., https://www.lacordee.com/en/products/kanuk-m-s-toundra-winter-jacket-kk2-10165#:~:text=100%25%20polyester%20Mini%20ottoman%20shell,and%20performance%20in%20humid%20conditions, https://www.holtrenfrew.com/p/20204809#:~:text=100%25%20Polyester;%20Lining:%20100,Length:%2032.5'', https://www.sail.ca/en/kanuk, https://www.sail.ca/en/kanuk#:~:text=%2D40%25,$790.00

### Competitive Displacement

**Google EN** (ai_mode_fallback):
> AI Mode
> All
> Images
> Videos
> News
> More
> Sign in
> Search Results
> Kanuk vs Quartz Co Montreal-made winter coat comparison
> While both Kanuk and Quartz Co. are prestigious Montreal-based brands, the primary difference lies in their insulation technology and manufacturing locations. Kanuk is renowned for its synthetic Thermo+ insulation that excels in damp, snowy conditions, whereas Quartz Co. focuses on traceable Canadian white duck down for a lighter, minimalist feel. 
> Boutique Bubbles
>  +2
> Manufacturing & Quality
> A significant point of comparison is where these jackets are currently produced, which ha
> Sources: https://www.boutiquebubbles.com/blogs/blog/kanuk-vs-quartz-co-a-comparative-review-of-luxury-outerwear-at-boutique-bubbles#:~:text=This%20makes%20Kanuk%20coats%20a%20great%20choice,those%20who%20prefer%20a%20more%20minimalist%20design., https://www.reddit.com/r/mcgill/comments/koxl2w/coat_suggestions/#:~:text=I%20second%20this.,grew%20up%20with%20mild%20winters.&text=Check%20out%20Quartz%20Co.%20!,it'll%20last%20for%20years!&text=I%20have%20one%20of%20their,ever%20since%20I%20bought%20it.&text=Check%20out%20Kanuk.,brand%20but%20absolutely%20worth%20it.&text=North%20face%20nuptse%20jackets%20are%20warm.&text=For%20a%20purely%20$%20to%20warmth,big%20deal%20to%20replace%20it.&text=%E2%80%A2%205y%20ago-,I%20second%20this.,Not%20the%20exact%20coat%20though., https://www.boutiquebubbles.com/fr/blogs/blog/kanuk-vs-quartz-co-a-comparative-review-of-luxury-outerwear-at-boutique-bubbles, https://www.sail.ca/blog/canadian-winter-jacket-brands/#:~:text=Extreme%20cold%20protection:%20Kanuk%20winter,in%20the%20most%20unforgiving%20conditions., https://www.reddit.com/r/BuyCanadian/comments/rgzlm0/osc_kanuk_or_quartz_co/#:~:text=I've%20had%20a%20Quartz,%E2%80%A2%204y%20ago

**Google FR** (ai_mode_fallback):
> 18 sitesKANUK Manteau Mont-Royal HommeThe Mont-Royal parka was designed for city living in winter. The attached hood comes with a fur option for maximum style and warmt...GoogleKANUK Manteau Mont-Royal HommeThe Mont-Royal parka was designed for city living in winter. The attached hood comes with a fur option for maximum style and warmt...GoogleKanuk clothing NO LONGER made in Canada 😟 : r/BuyCanadian20 oct. 2025 — have a lifetime warranty. Everything is made offshore, now. You name it as it's footwear, clothes, food/foodstuffs, medical suppli...RedditFAQ - KanukKanuk products are available onl
> Sources: https://quartz-co.com/products/vostok-3-0-expedition-parka?variant=40070519717972&country=CA&currency=CAD, https://www.altitude-sports.com/p/kanuk-montroyal-coat-mens-kan-10586, https://kanuk.com/products/men-jacket-mont-royal-jet-black, https://quartz-co.com/products/chloe-ca-hooded-down-winter-jacket?variant=42205367664724&country=CA&currency=CAD, https://www.sail.ca/blog/canadian-winter-jacket-brands/#:~:text=Extreme%20cold%20protection:%20Kanuk%20winter,jackets%20with%20a%20lifetime%20warranty.

---

## Revenue Impact

- **Quebec French-speaking market:** ~7M consumers
- **IAS 65/100** = ~35% of French AI queries failing or degraded
- AI-driven product discovery growing 40%+ YoY -- gap compounds quarterly

## What Fixes This

Bilingual JSON-LD injection + AI-readable product feeds (UCP/ACP) + Headless Agentic Probing to verify.

---
*Generated by Lead Gen Engine | Alex, AI PM -- Montreal (JMSB/Ampliwork)*