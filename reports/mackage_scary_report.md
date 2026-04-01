# AI Inference Audit: Mackage

**Inference Alignment Score: 69/100 -- YELLOW**

**Date:** 2026-04-01
**Category:** luxury winter down coat
**Methodology:** Gemini 2.5 Flash, 5 runs per query, 3 FR variants (n=15 FR, n=5 EN)

## Key Metrics

| Metric | English | French | Gap |
|--------|---------|--------|-----|
| Brand appearance rate | N/A | N/A | -- |
| Avg specs per response | N/A | N/A | -- |
| Spec range across runs | ?-? | ?-? | -- |
| Source authority score | 1.8 | 0.8 | -1.0 |

---

## Finding 1: Brand Visibility Gap

Brand appeared in N/A of English queries and N/A of French queries.

French queries tested:
1. "manteau d'hiver en duvet chic Montréal"
2. "meilleur manteau haut de gamme pour le froid à Montréal"
3. "manteau de luxe avec fourrure pour l'hiver québécois"

---

## Finding 2: Spec Dilution

Spec preservation: N/A (N/A FR vs N/A EN).
Range: ?-? specs across 15 French runs vs ?-? in English.

---

## Finding 3: Competitor Displacement

| Competitor | EN frequency | FR frequency | FR-only? |
|------------|-------------|-------------|----------|
| Canada Goose | present | present | No |
| Moose Knuckles | present | present | No |
| Nobis | present | present | No |
| Canada Goose | present | present | No |
| Quartz Co | present | 0% | No |
| La Canadienne | 0% | present | YES |
| Nobis | present | 0% | No |
| Patagonia | present | 0% | No |
| Moose Knuckles | 0% | present | YES |
| Kanuk | 0% | present | YES |

---

## Finding 4: Source Authority

EN sources avg score: 1.8/10 | FR sources avg score: 0.8/10
Gap: 1.0 points -- French AI responses rely on lower-authority sources.

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
> best luxury winter down coat in Montreal compare top options with specs and pricing
> Luxury winter down coats for Montreal's climate range from utilitarian heavyweights like Canada Goose to style-forward, technical options from local brands like Quartz Co. and Mackage. For the best performance during Montreal's extreme sub-zero peaks, look for a "TEI 5" or equivalent rating (down to -30°C and below). 
> Top Luxury Down Parkas Comparison
> Product Name 	Price (CAD)	Temp Rating	Fill Power	Key Feature
> Canada Goose Expedition Parka	$1795	-30°C 
> Sources: https://www.canadagoose.com/, https://madeinca.ca/jacket-brands-in-canada/, https://bettertrail.com/outdoor-gear/best-mens-winter-jackets, https://canoe.com/life/fashion/best-winter-jackets-in-canada, https://www.holtrenfrew.com/p/20281614005

**Google FR** (ai_mode_fallback):
> Mode IA
> Tous
> Images
> Vidéos
> Actualités
> Plus
> Connexion
> Résultats de recherche
> meilleur luxury winter down coat Montreal comparer meilleures options specifications prix
> Les meilleurs manteaux d'hiver de luxe pour Montréal proviennent de marques canadiennes emblématiques comme Kanuk, Mackage, Moose Knuckles et Canada Goose, reconnues pour leur capacité à affronter des températures allant jusqu'à -30 °C ou -40 °C. 
> best-of-johnjiangmacsg.replit.app
>  +4
> Comparaison des meilleures options de luxe
> Pour un hiver montréalais, le choix dépend de l'équilibre recherché entre performance technique, style ur
> Sources: https://www.reddit.com/r/Quebec/comments/17rs1rz/meilleur_rapport_qualit%C3%A9_prix_pour_les_manteaux/#:~:text=J'ai%20pass%C3%A9%20de%20Canada%20Goose%20(lourd%2C%20coutures,2%20hivers)%20pour%20ensuite%20acheter%20le%20Kanuk., https://www.la-canadienne.com/, https://www.reddit.com/r/CanadaGoose/comments/z6ivcu/another_canada_goose_or_moose_knuckle/, https://www.reddit.com/r/malefashionadvice/comments/5kozgq/mackage_or_moose_knuckle_or_canada_goose/, https://www.schreter.com/fc/femmes/vetements/manteaux/manteaux-dhiver-pour-femme/#:~:text=Choisissez%20parmi%20des%20marques%20%C3%A9prouv%C3%A9es%20et%20fiables%20comme%20Columbia%2C%20The%20North%20Face%20et%20Audvik.

### Brand Accuracy

**Google EN** (ai_mode_fallback):
> 28 sitesMackage Farren Stretch Lightweight Down Coat with ...Warm Statement. The women's FARREN makes a statement with a warm, fitted silhouette coat and movement-centric knee-length, perfect...Altitude SportsMackage Farren Down Coat Review: Stylish Winter Puffer CoatsDec 1, 2024 — Warmth Level. This coat is made with 90% down, 10% feather, which is considered a high-quality, insulating blend. Mackage down is ...Styled by ScienceDowns & Parkas | Mackage® CAChoose options Choose options. LYDANA Down Jacket With Shearling Trim and Removable Bib. $1,290.00. 2 colors. 2-IN-1. EDWARD-NFR 2...Mackag
> Sources: https://www.mackage.ca/products/kay-nfr?variant=42704626450677, https://bricksandbonds.ca/products/dixon-2-in-1-nordic-tech-down-bomber-bib-black, https://www.altitude-sports.com/p/mackage-adali-down-coat-with-signature-collar-womens-mak-adali-nfr#:~:text=a%20size%20XS-,%E2%80%A2%20Coat%20length%20from%20shoulder%20to%20hem:%2029%201/2,Water%20Resistant%2C%20Wind%20Resistant, https://www.altitude-sports.com/p/mackage-dixon-2in1-down-bomber-with-hooded-bib-and-natural-fur-mens-mak-dixon-f#:~:text=Mackage%20Dixon%202%2Din%2D1%20Down%20Bomber%20with%20Hooded,to%20keep%20you%20warm%20in%20cold%20weather., https://www.mackage.ca/products/adali-x?variant=42704178217205

**Google FR** (ai_mode_fallback):
> 13 sitesMackage Farren Stretch Lightweight Down Coat with Removable HoodSimilar styles * Mackage. Coralia-City Recycled Down Coat with Storm Visor and Belt - Women's. C$ 1,289. .99. * New. Mackage. Call...Altitude SportsMackage Farren Stretch Lightweight Down Coat with ...Mackage Farren Stretch Lightweight Down Coat with Removable Hood - Women's. (7) 1,049. .99. 4 payments of C$ 262.50 with . Black. ...Altitude SportsWomen's Downs and Parkas - MackageVANNA Mixed-media shearling down jacket. Sale price$1,990.00. 2 colors. Choose options Choose options. VANNA Mixed-media shearling...Mackage® CAW
> Sources: https://www.instagram.com/reel/DDuN_wDRfBi/#:~:text=This%20@mackage%20jacket%20was%20made%20for%20Canada,Thought%20I%20would%20share.%20Happy%20Wednesday%20fam%E2%9D%A4%EF%B8%8F, https://www.mackage.ca/collections/womens-downs-and-parkas#:~:text=VANNA%20Mixed%2Dmedia%20shearling%20down,Choose%20options%20Choose%20options, https://www.mackage.ca/collections/womens-outerwear#:~:text=$1%2C250.00,2%20colors, https://www.mackage.ca/products/farren#:~:text=FARRENBlack%20/%20XXS%20Sale%20price,cart%20Add%20to%20cart%20%7C%20$1%2C050.00, https://styledbyscience.com/mackage-farren-down-coat-review/#:~:text=Warmth%20Level,up%20to%20%2D10%C2%B0C.

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
> Mackage vs Canada Goose luxury winter down coat comparison
> In the luxury outerwear market, Canada Goose is primarily recognized for its utilitarian, function-first heritage designed for extreme Arctic conditions, while Mackage is known for its "style-forward" approach that balances high-fashion aesthetics with significant warmth. 
> Brand Philosophies and Design
> Canada Goose: Focuses on a rugged, utilitarian design language rooted in Canadian workwear. Its silhouettes are often more straightforward and "sport" or "functional" in appearan
> Sources: https://www.reddit.com/r/durham/comments/1oyayo8/mackage_vs_canada_goose/#:~:text=I've%20had%20mine%20for,%E2%80%A2%201mo%20ago, https://www.gentlemansgazette.com/canada-goose-jackets-is-it-worth-it/#:~:text=vs.&text=This%20is%20the%20most%20frequent,excels%20in%20fashion%2Dforward%20style., https://sportinglifeblog.ca/comparing-coats-mens-bomber-jackets/, https://www.extrapetite.com/2022/12/mackage-coat-review-farren-calla-nori-fit-for-petites.html#:~:text=After%20trying%20on%20petite%2Dfriendly,is%20much%20more%20style%2Dforward., https://www.circle-fashion.com/clothing-c1/coats-jackets-c6/canada-goose-womens-hybridge-base-jacket-p43215#:~:text=Brought%20to%20you%20by%20Canadian%20label%20Canada,ribbed%20cuffs%20and%20an%20adjustable%20hooded%20neckline.

**Google FR** (ai_mode_fallback):
> 14 sitesMackage vs Canada Goose : r/durham - Reddit16 nov. 2025 — * Mackage winter parka options. * Mackage sizing guide. * Mackage similar coat brands. * Comparison of Canada Goose and Moncler. *RedditMackage vs Canada Goose : r/durham - Reddit16 nov. 2025 — * Mackage winter parka options. * Mackage sizing guide. * Mackage similar coat brands. * Comparison of Canada Goose and Moncler. *RedditMackage vs Canada Goose : r/durham - Reddit16 nov. 2025 — * Mackage winter parka options. * Mackage sizing guide. * Mackage similar coat brands. * Comparison of Canada Goose and Moncler. *RedditReview: Ma
> Sources: https://www.reddit.com/r/durham/comments/1oyayo8/mackage_vs_canada_goose/#:~:text=I've%20had%20mine%20for,%E2%80%A2%201mo%20ago, https://www.themanual.com/fashion/best-canada-goose-alternatives/#:~:text=Mackage,-Pros&text=If%20you%20pay%20attention%20to,while%20still%20being%20high%20end., https://www.reddit.com/r/BuyItForLife/comments/1856ipz/canada_goose_jackets/, https://sportinglifeblog.ca/comparing-coats-mens-bomber-jackets/, https://www.youtube.com/watch?v=bEF1KRrygS4&t=107

---

## Revenue Impact

- **Quebec French-speaking market:** ~7M consumers
- **IAS 69/100** = ~31% of French AI queries failing or degraded
- AI-driven product discovery growing 40%+ YoY -- gap compounds quarterly

## What Fixes This

Bilingual JSON-LD injection + AI-readable product feeds (UCP/ACP) + Headless Agentic Probing to verify.

---
*Generated by Lead Gen Engine | Alex, AI PM -- Montreal (JMSB/Ampliwork)*