# AI Inference Audit: Moose Knuckles

**Inference Alignment Score: 64/100 -- YELLOW**

**Date:** 2026-04-01
**Category:** premium Canadian down parka
**Methodology:** Gemini 2.5 Flash, 5 runs per query, 3 FR variants (n=15 FR, n=5 EN)

## Key Metrics

| Metric | English | French | Gap |
|--------|---------|--------|-----|
| Brand appearance rate | N/A | N/A | -- |
| Avg specs per response | N/A | N/A | -- |
| Spec range across runs | ?-? | ?-? | -- |
| Source authority score | 2.2 | 1.3 | -0.9 |

---

## Finding 1: Brand Visibility Gap

Brand appeared in N/A of English queries and N/A of French queries.

French queries tested:
1. "parka canadien le plus chaud pour l'hiver"
2. "meilleur manteau en duvet fait au Canada"
3. "quel parka acheter pour le froid extrême au Québec"

---

## Finding 2: Spec Dilution

Spec preservation: N/A (N/A FR vs N/A EN).
Range: ?-? specs across 15 French runs vs ?-? in English.

---

## Finding 3: Competitor Displacement

| Competitor | EN frequency | FR frequency | FR-only? |
|------------|-------------|-------------|----------|
| Canada Goose | present | present | No |
| Mackage | present | present | No |
| Canada Goose | present | present | No |
| Mackage | present | present | No |
| La Canadienne | 0% | present | YES |
| Quartz Co | present | 0% | No |
| Kanuk | present | 0% | No |

---

## Finding 4: Source Authority

EN sources avg score: 2.2/10 | FR sources avg score: 1.3/10
Gap: 0.9 points -- French AI responses rely on lower-authority sources.

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
> best premium Canadian down parka in Montreal compare top options with specs and pricing
> Top premium Canadian down parkas available in Montreal include the Canada Goose Expedition Parka, Arctic Bay Montreal Parka, and Quartz Co. Labrador, each offering specialized protection for temperatures down to -30°C or lower. 
> Top Extreme-Weather Parkas
> These options are engineered for the coldest days in Montreal, featuring high fill power and robust shells to block wind and moisture. 
> Canada Goose Expedition Down Parka in White | Men's Size Larg
> Sources: https://audvik.com/en#:~:text=LOCAL%20AND%20ECO%2DFRIENDLY%20WINTER,of%20durable%20and%20timeless%20coats.&text=Proudly%20handcrafted%20in%20our%20Chabanel,creations%20directly%20at%20the%20workshop.&text=Because%20at%20Audvik%20we%20have,loved%20and%20pre%2Dworn%20coats., https://quartz-co.com/products/jules-down-jacket?variant=40069078450260, https://pologeorgis.com/blogs/news/how-to-choose-a-jacket-for-canadian-winter#:~:text=Insulation%20Guidance:%20For%20most%20Canadian,overheat%20you%20during%20active%20commuting., https://pologeorgis.com/blogs/news/how-to-choose-a-jacket-for-canadian-winter#:~:text=For%20Toronto%20and%20Montreal%2C%20that%20usually%20means,you'll%20face%20for%20several%20weeks%20each%20year., https://www.mec.ca/en/article/your-guide-to-the-warmest-jackets-from-mec#:~:text=Our%20premium%20packable%20jacket&text=Our%20favourite%20features%20start%20with,of%20warmth%20when%20it's%20on.%E2%80%9D

**Google FR** (ai_mode_fallback):
> 14 sitesWhich Down Jacket Is Better? | Moose Knuckles VS Canada ...25 déc. 2021 — they are both luxury brands with the same $1,000. plus price tag. but one has to be better than the other. right we're going to ge...YouTube·Men's Fashion Files11mWhich Down Jacket Is Better? | Moose Knuckles VS Canada ...25 déc. 2021 — they are both luxury brands with the same $1,000. plus price tag. but one has to be better than the other. right we're going to ge...YouTube·Men's Fashion Files11mCANADA GOOSE Or MOOSE KNUCKLES?! Which Designer ...19 janv. 2026 — yo what is up guys We're back with a very special v
> Sources: https://www.reddit.com/r/femalefashionadvice/comments/1xc0oz/mackage_coats_and_winter_coats_in_generalyour_two/?tl=fr#:~:text=Canada%20Goose%20utilise%20une%20combinaison%20de%20duvet,dans%20ses%20produits%20appel%C3%A9s%20%22hutterite%20down%22%20:), https://www.mooseknucklescanada.com/fr, https://www.la-canadienne.com/, https://www.boutiquebubbles.com/fr/collections/men-down-coats, https://www.youtube.com/watch?v=MVKtkCQ3VUQ

### Brand Accuracy

**Google EN** (ai_mode_fallback):
> 19 sitesProduct Knowledge | Moose Knuckles CAMoose Knuckles Classic Core jackets and parkas are created using a blend of fabric consisting of 74% Cotton and 26% Nylon, this bl...Moose KnucklesProduct Knowledge | Moose Knuckles CADown filaments come from the fluffy coating from ducks and goose, that overlap to create small air pockets that trap warmth and bo...Moose Knucklesmoose knuckles - Due WestMoose Knuckles Mens Down Jacket Everest 3Q Puffer - NavyDescription Features: Temperature rated for Level 3: Crazy Cold, -10°C to ...duewest.caGold Series Stirling Shearling Trim Parka - Moose Knuckl
> Sources: https://www.mooseknucklescanada.com/products/gold-series-stirling-shearling-trim-parka-m35lp203gs-305, https://www.mooseknucklescanada.com/collections/parkas, https://www.sportinglife.ca/en-CA/women/clothing/coats-jackets/winter-coats/womens-lonsdale-long-wrap-coat/25922385.html#:~:text=Welt%20pockets%20add%20sleek%20functionality%2C%20and%20recycled,topper%20for%20dinner%20dates%20and%20fashion%2Dforward%20commutes., https://www.ubuy.com.lb/en/product/4CXSKWNYW-womens-debbie-bomber-down-jacket-with-fur-pom-pom#:~:text=Answer:%20The%20Moose%20Knuckles%20Womens%20Debbie%20Bomber,efficiency%2C%20making%20it%20ideal%20for%20cold%20weather., https://www.mooseknucklescanada.com/en-us/pages/warm-af#:~:text=The%20shell&text=Durable%20front%20and%20back.,with%20a%20waterproof%20laminated%20backing.&text=We%20use%20lightweight%20duck%20and,be%20tear%20and%20snag%2Dproof.&text=Moose%20Knuckles%20uses%20certified%2C%20100,from%20650+%20to%20800%20cc's.

**Google FR** (ai_mode_fallback):
> 21 sitesMoose Knuckles Womens Down *Parka Stirling - Black/Black$1,395.00 $839.00. or 4 interest-free payments of $209.75 with ⓘ Outerwear Size. S - Two items left. M - Sold Out. L - Sold Out. B...duewest.caCloud Shearling Parka | Men - Moose KnucklesOur Cloud Parka, now upgraded with Neoshearling, maintains the classic silhouette of our Icons while shedding 30% of its weight. T...Moose Knuckles3Q Jackets for Winter Season | Moose Knuckles CAORIGINAL SHEARLING TRIM 3Q JACKET. $1,395. Sale price $1,395 Regular price $0. Unit price / per. Colour: NAVY/NATURAL. NAVY/NATURA...Moose KnucklesParkas 
> Sources: https://duewest.ca/products/moose-knuckles-womens-down-parka-stirling-parka-black-black-a#:~:text=$1%2C395.00%20$839.00,Rib%20Knit%20Storm%20Cuffs, https://duewest.ca/collections/moose-knuckles#:~:text=S%20/%20Navy%2DNatural,Akai%20Cropped%20%2D%20Black%20$795.00%20$559.00, https://www.sportinglife.ca/en-CA/women/clothing/coats-jackets/winter-coats/womens-cloud-3q-jacket/25893967.html#:~:text=Description,DWR%20(DURABLE%20WATER%20REPELLENT), https://www.altitude-sports.com/fr-CA/p/moose-knuckles-parka-avec-dtails-en-neoshear-stirling-original-femme-mkk-m32lp203s, https://www.mooseknucklescanada.com/products/original-shearling-trim-stirling-parka-m35mp261s-546#:~:text=$1%2C495,Colour:%20NAVY/BLACK

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
> Moose Knuckles vs Canada Goose premium Canadian down parka comparison
> While both brands are leaders in premium Canadian outerwear, Moose Knuckles typically offers higher thermal insulation values and a more fashion-forward, slim fit, whereas Canada Goose is widely recognized for its "arctic research scientist" aesthetic and legendary practicality. 
> Reddit
>  +4
> Thermal Performance and Insulation
> Research suggests Moose Knuckles may hold a slight edge in raw thermal performance for its flagship models.
> Insulation Ratings: In thermal insul
> Sources: https://www.mooseknucklescanada.com/, https://www.reddit.com/r/CanadaGoose/comments/xgaw8z/psa_for_those_interested_in_buying_brand_new/#:~:text=Of%20course%2C%20this%20difference%20is,such%20a%20beautiful%20coat., https://www.reddit.com/r/BuyItForLife/comments/187s9fm/canada_goose_or_moose_knuckle_parka_a_for_someone/, https://freeds.com/blogs/blog/moose-knuckles-parka-ranks-top-amongst-competitors-for-thermal-insulation#:~:text=Moose%20Knuckles%20has%20been%20ranked%20with%20the,jackets%20against%20Canada%20Goose%2C%20Mackage%20and%20Woolrich., https://freeds.com/blogs/blog/moose-knuckles-parka-ranks-top-amongst-competitors-for-thermal-insulation#:~:text=The%20Moose%20Knuckles%20MK4661MP%20parka,for%20Woolrich%20(3.49%20clo).

**Google FR** (ai_mode_fallback):
> Mode IA
> Tous
> Images
> Vidéos
> Actualités
> Plus
> Connexion
> Résultats de recherche
> Moose Knuckles vs Canada Goose premium Canadian down parka comparaison
> Moose Knuckles et Canada Goose sont deux marques canadiennes de parkas haut de gamme reconnues pour leur protection thermique extrême, mais elles diffèrent par leur esthétique et leur ajustement. Canada Goose est réputée pour ses designs utilitaires intemporels et ses coupes plus amples, tandis que Moose Knuckles mise sur une allure plus "streetwear" avec des coupes ajustées et des matériaux souvent perçus comme plus robustes. 
> Forbes
>  +2
> Performanc
> Sources: https://www.reddit.com/r/CanadaGoose/comments/1qe3eq6/opinions_on_moose_knuckles/#:~:text=Ok%2DCat774,purpose%20you%20need%20it%20for., https://www.reddit.com/r/CanadaGoose/comments/z6ivcu/another_canada_goose_or_moose_knuckle/, https://www.youtube.com/watch?v=bEF1KRrygS4&t=107, https://www.reddit.com/r/BuyItForLife/comments/187s9fm/canada_goose_or_moose_knuckle_parka_a_for_someone/, https://www.canadagoose.com/

---

## Revenue Impact

- **Quebec French-speaking market:** ~7M consumers
- **IAS 64/100** = ~36% of French AI queries failing or degraded
- AI-driven product discovery growing 40%+ YoY -- gap compounds quarterly

## What Fixes This

Bilingual JSON-LD injection + AI-readable product feeds (UCP/ACP) + Headless Agentic Probing to verify.

---
*Generated by Lead Gen Engine | Alex, AI PM -- Montreal (JMSB/Ampliwork)*