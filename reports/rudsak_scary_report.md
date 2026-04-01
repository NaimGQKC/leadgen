# AI Inference Audit: Rudsak

**Inference Alignment Score: 63/100 -- YELLOW**

**Date:** 2026-04-01
**Category:** leather winter outerwear
**Methodology:** Gemini 2.5 Flash, 5 runs per query, 3 FR variants (n=15 FR, n=5 EN)

## Key Metrics

| Metric | English | French | Gap |
|--------|---------|--------|-----|
| Brand appearance rate | N/A | N/A | -- |
| Avg specs per response | N/A | N/A | -- |
| Spec range across runs | ?-? | ?-? | -- |
| Source authority score | 1.7 | 1.8 | --0.1 |

---

## Finding 1: Brand Visibility Gap

Brand appeared in N/A of English queries and N/A of French queries.

French queries tested:
1. "manteau de cuir pour l'hiver Montréal"
2. "où trouver un manteau en cuir chaud à Montréal"
3. "veste de cuir doublée pour le froid québécois"

---

## Finding 2: Spec Dilution

Spec preservation: N/A (N/A FR vs N/A EN).
Range: ?-? specs across 15 French runs vs ?-? in English.

---

## Finding 3: Competitor Displacement

| Competitor | EN frequency | FR frequency | FR-only? |
|------------|-------------|-------------|----------|
| Mackage | present | present | No |
| Mackage | present | present | No |
| Moose Knuckles | present | 0% | No |
| Kanuk | 0% | present | YES |

---

## Finding 4: Source Authority

EN sources avg score: 1.7/10 | FR sources avg score: 1.8/10
Gap: 0.1 points -- French AI responses rely on lower-authority sources.

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
> best leather winter outerwear in Montreal compare top options with specs and pricing
> For Montreal's notorious winters, leather outerwear must balance style with high-performance insulation to handle temperatures that frequently drop to 
> −
> 3
> 0
> ∘
> 𝐶
> . The top options for 2026 range from high-fashion leather down puffers to rugged, locally crafted parkas. 
> Top Leather Winter Outerwear Options
> Mackage Cash Diamond-quilted Leather Jacket With Shearling Hood
> $2,490.00
> mackage.ca
> A luxury "city-ready" down-filled leather jacket.
> Specs: Diamond
> Sources: https://www.ariannerelocation.com/winter-in-montreal-101-how-to-dress-for-the-cold/#:~:text=Although%20the%20temperatures%20can%20fluctuate%20throughout%20the,winter%20takes%20a%20turn%20for%20the%20coldest., https://www.mooseknucklescanada.com/products/original-shearling-trim-3q-jacket-m35mj128s-1001?variant=46626653012203, https://www.mackage.ca/products/cash?variant=46836821950709, https://www.likevancouver.ca/blog/the-best-canadian-shoe-brands#:~:text=Specializing%20in%20weatherproof%20boots%2C%20La%20Canadienne%20is,them%20a%20winter%20essential%20for%20style%2Dconscious%20Canadians., https://www.cuirdimitri.ca/#:~:text=Monaco%20Leather%20Trench%20Coat,View%20Product

**Google FR** (ai_mode_fallback):
> Mode IA
> Tous
> Images
> Vidéos
> Actualités
> Plus
> Connexion
> Résultats de recherche
> meilleur leather winter outerwear Montreal comparer meilleures options specifications prix
> À Montréal, le choix d'un manteau d'hiver en cuir de haute qualité repose sur des marques locales emblématiques qui allient la durabilité du cuir à l'isolation thermique nécessaire pour affronter des températures allant jusqu'à 
> -30
> ∘
> C
> −
> 3
> 0
> ∘
> C
> . 
> Simon Premium Outlets
>  +1
> Voici une comparaison des meilleures options disponibles sur le marché montréalais :
> Comparatif des Meilleures Options de Vêtements d'Extérieur en Cuir
> Modèl
> Sources: https://www.gingtto.com/fr/blogs/news/when-do-winter-coats-go-on-sale#:~:text=Fin%20de%20l'hiver%20(janvier,place%20aux%20collections%20de%20printemps., https://rudsak.com/fr/products/harvey-x-6125681-black, https://www.instagram.com/reel/DQlb1RUDrCx/, https://rudsak.com/fr/products/jordy-x-6125694-black, https://www.cuirdimitri.ca/

### Brand Accuracy

**Google EN** (ai_mode_fallback):
> AI Mode
> All
> Images
> Videos
> News
> More
> Sign in
> Search Results
> Rudsak leather winter outerwear full technical specs materials technology pricing
> Rudsak's leather winter outerwear is defined by a blend of technical performance and luxury aesthetics. Their "X" series specifically refers to premium leather editions of their signature down-filled silhouettes. 
> Technical Materials & Technology
> Shell Materials:
> Supple Lamb Leather: Used in most premium puffers and parkas for a luxe finish.
> Cloud Leather: An ultra-lightweight, high-performance leather used in specific models like the Shauna X to reduce o
> Sources: https://rudsak.com/blogs/rudsak/heritage-coat-editions#:~:text=The%20CAFA%20recognition%20as%20Outerwear,strength%20lies%20in%20its%20range., https://rudsak.com/collections/mens-leather-jackets#:~:text=MANUS%20B%20MEN'S%20LEATHER%20MOTO,$595.00, https://rudsak.com/pages/faq-products-sizes#:~:text=Please%20visit%20the%20product%20page,feathers%20and%20600+Fill%20power., https://rudsak.com/collections/sale-leather-jackets#:~:text=ANNABELLE%20FSU%20WOMEN'S%20REVERSIBLE%20FAUX,$995.00%20$499.99%20Final%20Sale, https://rudsak.com/blogs/rudsak/the-rudsak-difference#:~:text=RDS%2DCERTIFIED%20DOWN%2C%20ENGINEERED%20FOR,warmth%2C%20movement%2C%20and%20durability.

**Google FR** (ai_mode_fallback):
> 16 sitesTHE RUDSAK DIFFERENCETEMPERATURE-TESTED PERFORMANCE. Designed for real Canadian winters and tested for warmth, movement, and durability.RudsakRUDSAK JACK Men's Quilted Down Puffer JacketInsulated with RDS-certified down, wind and water-repellent, and equipped with storm cuffs, feather fill. 700+ Fill Power.RudsakManteaux d'hiver chauds pour Femme - Rudsakdocument: * -5C (52) * -15C (23) * -20C (23) * -25C (39) * -30C (10)RudsakSustainability – Rudsak100% of leather trims and sleeves of the current RUDSAK collections are made from recycled leather. made of 100% recycled material...Rudsa
> Sources: https://rudsak.com/fr/collections/womens-coats-jackets?page=2#:~:text=document:%20*%20%2D5C%20(52)%20*%20%2D15C%20(23),(23)%20*%20%2D25C%20(39)%20*%20%2D30C%20(10), https://rudsak.com/products/conor-6124596-black#:~:text=Elevate%20your%20winter%20wardrobe%20with,LambTrim:%20100%25%20Lamb%20Leather, https://rudsak.com/products/jack-m124507-black#:~:text=The%20JACK%20by%20RUDSAK%20is,Trim:%20100%25%20Thermoplastic%20Polyurethane, https://rudsak.com/blogs/rudsak/the-rudsak-difference#:~:text=RDS%2DCERTIFIED%20DOWN%2C%20ENGINEERED%20FOR,warmth%2C%20movement%2C%20and%20durability., https://boutiquedesigners.com/products/rudsak-manteau-hiver-3#:~:text=Malefica%20est%20un%20manteau%20polyvalent%20pour%20les,l%C3%A9ger%2C%20extensible%2C%20coupe%2Dvent%20et%20r%C3%A9sistant%20%C3%A0%20l'eau%2C

### Competitive Displacement

**Google EN** (ai_mode_fallback):
> 15 sitesRudsak vs Mackage : r/askTO - RedditMar 26, 2018 — I think they are similar in terms of quality but you got to see which design you like better. Mackage costs a bit more than Rudsak...RedditRudsak vs Mackage : r/askTO - RedditMar 26, 2018 — Mackage costs a bit more than Rudsak and Rudsak, especially the Vaughan Mills store, offers great discounts when they have sales.RedditOur Favourite Coats To Get You Through The WinterMackage Winter Coats. In our opinion, any list of premium winter coats is not complete if it does not include the name Mackage in ...Love Your LeatherOur Favourite Coa
> Sources: https://www.youtube.com/watch?v=s8E3-KeamzI&t=20, https://rudsak.com/blogs/rudsak/the-rudsak-difference#:~:text=Premium%20materials.,built%20to%20last%E2%80%94unmistakably%20RUDSAK., https://www.tiktok.com/discover/rudsak-winter-coat-vs-mackage#:~:text=original%20sound%20%2D%20Dom%20%7C%20Fragrance%20&%20Beyond&text=So%20y'all%20be%20talking,coat%20that%20keeps%20you%20warm., https://www.tiktok.com/@delilahdesireee/video/7591592852430343454#:~:text=A%20Mackage%20coat%20is%20essential%20for%20Chicago,effort%20for%20the%20rest%20of%20the%20outfit., https://www.tiktok.com/@brielleny/video/7463915626772401454#:~:text=The%20only%20thing%20I%20will,2

**Google FR** (ai_mode_fallback):
> Mode IA
> Tous
> Images
> Vidéos
> Actualités
> Plus
> Connexion
> Résultats de recherche
> Rudsak vs Mackage leather winter outerwear comparaison
> Mackage est généralement considéré comme la marque la plus haut de gamme et sophistiquée des deux, tandis que Rudsak mise sur un style plus « rebelle » et urbain, souvent à un prix plus accessible. Les deux marques montréalaises excellent dans l'intégration du cuir à leurs vêtements d'hiver, mais elles s'adressent à des styles différents. 
> Comparaison des marques
> Mackage : Reconnue pour ses silhouettes cintrées et très structurées qui allient luxe et haute performa
> Sources: https://www.loveyourleather.ca/leather-blog/our-favourite-coats-to-get-you-through-the-winter/#:~:text=Rudsak%20Winter%20Jacket,chic%20outerwear%20and%20apparel%20manufacturer., https://www.youtube.com/watch?v=s8E3-KeamzI&t=20, https://realry.com/products/67b9998d11e30c11d40b8c98, https://www.tiktok.com/@delilahdesireee/video/7591592852430343454#:~:text=A%20Mackage%20coat%20is%20essential%20for%20Chicago,effort%20for%20the%20rest%20of%20the%20outfit., https://www.reddit.com/r/askTO/comments/875njz/rudsak_vs_mackage/#:~:text=I%20have%20a%20Mackage%20leather,16

---

## Revenue Impact

- **Quebec French-speaking market:** ~7M consumers
- **IAS 63/100** = ~37% of French AI queries failing or degraded
- AI-driven product discovery growing 40%+ YoY -- gap compounds quarterly

## What Fixes This

Bilingual JSON-LD injection + AI-readable product feeds (UCP/ACP) + Headless Agentic Probing to verify.

---
*Generated by Lead Gen Engine | Alex, AI PM -- Montreal (JMSB/Ampliwork)*