# AI Inference Audit: SSENSE

**Inference Alignment Score: 60/100 -- YELLOW**

**Date:** 2026-04-01
**Category:** luxury designer winter coat
**Methodology:** Gemini 2.5 Flash, 5 runs per query, 3 FR variants (n=15 FR, n=5 EN)

## Key Metrics

| Metric | English | French | Gap |
|--------|---------|--------|-----|
| Brand appearance rate | 60% (3/5) | 53% (8/15) | -7% |
| Avg specs per response | 9.8 | 5.3 | -46% |
| Spec range across runs | 5-14 | 0-12 | -- |
| Source authority score | 1.3 | 2.2 | --0.9 |

---

## Finding 1: Brand Visibility Gap

Brand appeared in 60% of English queries but only 53% of French queries.

French queries tested:
1. "où acheter un manteau de luxe à Montréal"
2. "boutique en ligne mode haut de gamme Montréal"
3. "meilleurs manteaux griffés hiver Montréal"

---

## Finding 2: Spec Dilution

54% of technical specs preserved in French (5.3 vs 9.8).
Range: 0-12 specs across 15 French runs vs 5-14 in English.

---

## Finding 3: Competitor Displacement

| Competitor | EN frequency | FR frequency | FR-only? |
|------------|-------------|-------------|----------|
| Acne Studios | 0% | 7% | YES |
| Aldo | 20% | 0% | No |
| Arc'teryx | 0% | 7% | YES |
| Balenciaga | 0% | 40% | YES |
| Bottega Veneta | 0% | 13% | YES |
| Burberry | 0% | 27% | YES |
| COS | 0% | 13% | YES |
| Canada Goose | 100% | 60% | No |
| Celine | 20% | 0% | No |
| Dior | 0% | 20% | YES |
| Farfetch | 0% | 7% | YES |
| Fendi | 0% | 7% | YES |
| Gucci | 0% | 27% | YES |
| Holt Renfrew | 100% | 80% | No |
| Loewe | 0% | 27% | YES |
| Louis Vuitton | 0% | 27% | YES |
| Mackage | 100% | 60% | No |
| Maje | 0% | 13% | YES |
| Max Mara | 0% | 33% | YES |
| Moncler | 100% | 67% | No |
| Moose Knuckles | 100% | 47% | No |
| Nobis | 100% | 47% | No |
| Nordstrom | 20% | 0% | No |
| Off-White | 0% | 20% | YES |
| Prada | 0% | 27% | YES |
| Quartz Co | 0% | 13% | YES |
| Rudsak | 0% | 13% | YES |
| Saint Laurent | 0% | 27% | YES |
| Saks Fifth Avenue | 20% | 0% | No |
| Sandro | 0% | 7% | YES |
| Sentaler | 0% | 13% | YES |
| Simons | 60% | 80% | No |
| The North Face | 0% | 7% | YES |
| Woolrich | 0% | 20% | YES |

---

## Finding 4: Source Authority

EN sources avg score: 1.3/10 | FR sources avg score: 2.2/10
Gap: 0.9 points -- French AI responses rely on lower-authority sources.

---

## Bonus: Google AI Mode (Live Search)

Results captured via live Chromium browser with Montreal geolocation.

### Generic Discovery

**Google EN** (ai_mode_fallback):
> 20 sitesAltitude SportsOct 16, 2024 — 4. Mackage Launched in 1999 by a Montreal couple, Mackage is a high-end brand that believes the coat is the integral part of your ...Altitude Sports10 luxe hot spots to shop in Bloor-YorkvilleAug 18, 2021 — It's known as the go-to brand among the world's elite, high-quality enough to be cleared as a classified luxury brand, with each j...Toronto LifeKanuk vs. Quartz Co: A Comparative Review of Luxury Outerwear at Boutique BubblesJul 15, 2023 — As the chill of winter approaches, the quest for the perfect coat becomes a top priority. Two brands that have bee
> Sources: https://www.altitude-sports.com/blog/mackage-coats-for-winter-warmth#:~:text=Mackage%20coats%20and%20jackets%20help%20make%20your,sense%20of%20style%E2%80%94urban%2C%20sleek%20and%20thoroughly%20modern., https://www.moorer.clothing/us/en/men/outerwear/parka/sapporo-gf-darkblu-MOUPA100021TEPA012U0402.html?Country=US&keeplocale=true&pid=418057144479119, https://www.meurice.nyc/journal/2018/11/5/moncler-vs-canadagoose#:~:text=In%20our%20opinion%2C%20this%20is,their%20inventive%20and%20designer%20aesthetic., https://www.canadagoose.com/, https://torontolife.com/shopping/10-luxe-hot-spots-to-shop-in-bloor-yorkville/#:~:text=It's%20known%20as%20the%20go%2Dto%20brand%20among,months%20away%2C%20set%20your%20sights%20on%20Moncler.

**Google FR** (ai_mode_fallback):
> Mode IA
> Tous
> Images
> Vidéos
> Actualités
> Plus
> Connexion
> Résultats de recherche
> meilleur luxury designer winter coat Montreal comparer meilleures options specifications prix
> Pour un hiver à Montréal, les meilleurs manteaux de luxe combinent une isolation thermique de haute performance (souvent certifiée pour -30°C) avec des designs sophistiqués. Les marques montréalaises comme Mackage et Kanuk sont particulièrement réputées pour leur équilibre entre style urbain et résistance au froid extrême. 
> Reddit
>  +2
> Comparaison des Parkas de Luxe (Modèles Phares)
> Modèle 	Marque	Caractéristiques Clés	Usage Id
> Sources: https://www.reddit.com/r/Quebec/comments/17rs1rz/meilleur_rapport_qualit%C3%A9_prix_pour_les_manteaux/#:~:text=J'ai%20pass%C3%A9%20de%20Canada%20Goose%20(lourd%2C%20coutures,2%20hivers)%20pour%20ensuite%20acheter%20le%20Kanuk., https://www.la-canadienne.com/, https://www.instagram.com/reel/DQxPYEGCTed/, https://www.outdoorgearlab.com/best-winter-jacket, https://canoe.com/life/fashion/best-winter-jackets-in-canada

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
> SSENSE luxury designer winter coat full technical specs materials technology pricing
> At SSENSE, luxury designer winter coats range from high-performance technical parkas to sartorial wool overcoats, with prices typically between $430 CAD and $6,290 CAD. Leading technical brands like Moncler and The North Face utilize specialized insulation like DIST-certified goose down and weatherproof technologies such as GORE-TEX and non-PFC DWR coatings. 
> SSENSE
>  +4
> Technical Specifications & Materials
> The technical builds on SSENSE focus on balanc
> Sources: https://www.ssense.com/en-ca/men/coats#:~:text=Black%202L%20Nylon%20GORE%2DTEX,WOOYOUNGMI, https://www.ssense.com/en-ca/women/product/totme/black-classic-winter-coat/18625931, https://www.ssense.com/en-sa/editorial/market/best-winter-coats#:~:text=SSENSE%20says:%20Norse%20Projects%20added,from%20Loro%20Piana%20to%20shine., https://www.ssense.com/en-ca/men/coats#:~:text=Beige%20Regular%2DFit%20Wool%20&%20Cashmere,$1985%20$3970, https://www.ssense.com/en-ca/men/coats#:~:text=Black%20Wool%20Blend%20Half%20Coat,$2195

**Google FR** (ai_mode_fallback):
> Mode IA
> Tous
> Images
> Vidéos
> Actualités
> Plus
> Connexion
> Résultats de recherche
> SSENSE luxury designer winter coat specifications techniques completes materiaux technologie prix
> Les manteaux d'hiver de luxe disponibles sur SSENSE intègrent des matériaux de haute performance et des technologies de pointe pour allier esthétique et protection thermique extrême. Les prix varient généralement de 500 CAD pour des modèles techniques d'entrée de gamme jusqu'à plus de 4 000 CAD pour des pièces de créateurs haut de gamme. 
> SSENSE
>  +3
> Matériaux et Technologies de Pointe
> Les designers sur SSENSE utilisent des
> Sources: https://www.ssense.com/en-ca/women/jackets-coats?gclid=Cj0KEQjwvOC5BRCb_8yNmZ_ls9IBEiQACTz8vmFLi8S3JDM22VnQmvxIg_wZ47pMoOBko13TIj_fwUwaAg1a8P8HAQ&sort=price-asc&sizes=S&page=7#:~:text=Brown%20Reedition%20Vinyl%20Jacket,Beige%20Igelle%20Down%20Jacket, https://www.ssense.com/en-ca/editorial/market/best-winter-coats#:~:text=SSENSE%20says:%20Canada%20Goose%20is,both%20urban%20and%20extreme%20lifestyles., https://www.ssense.com/en-ca/editorial/market/best-technical-jackets-fall-winter#:~:text=C.P.%20Company%20Black%20Baffled%20Down,Herno%20Blue%20Laminar%20Down%20Jacket, https://www.ssense.com/en-ca/women/jackets-coats?gclid=Cj0KEQjwvOC5BRCb_8yNmZ_ls9IBEiQACTz8vmFLi8S3JDM22VnQmvxIg_wZ47pMoOBko13TIj_fwUwaAg1a8P8HAQ&colors=black&sort=price-desc&page=4#:~:text=$817%20$1900,$765, https://www.ssense.com/en-ca/men/coats#:~:text=$3105-,Dries%20Van%20Noten,WOOYOUNGMI

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
> SSENSE vs Farfetch luxury designer winter coat comparison
> SSENSE and Farfetch are both legitimate luxury retailers, but they operate on fundamentally different business models that affect your shopping experience for winter coats. SSENSE is a traditional retailer that buys and stocks its own inventory, allowing for better control over photography, descriptions, and shipping speed. Farfetch is a global marketplace that connects you to hundreds of independent boutiques worldwide, offering a significantly larger and more diverse selection
> Sources: https://www.ssense.com/en-ca/editorial/market/best-winter-coats#:~:text=SSENSE%20says:%20Canada%20Goose%20is,both%20urban%20and%20extreme%20lifestyles., https://www.reddit.com/r/viviennewestwood/comments/1o4jf8n/farfetch_or_ssense/#:~:text=Not%20sure%20if%20Farfetch%20does,from%20SSENSE%20to%20be%20authentic.&text=I%20ordered%20this%20bag%2C%20in,papers%20and%20a%20dust%20bag.&text=If%20you're%20in%20the,due%20to%20the%20US%20gov.&text=I've%20bought%20from%20both,I%20prefer%20SSENSE%20tho.&text=Farfetch%20is%20usually%20better%20for,they%20stock%20authentic%20Westwood%20menswear., https://www.reddit.com/r/montreal/comments/1qmzrcd/what_is_your_experience_returning_stuff_at_ssense/#:~:text=I%20ordered%20clothes%20online%20on,t%20do%20is%20so%20frustrating., https://thewalrus.ca/inside-the-ssense-fiasco/#:~:text=J'Nae%20Phillips%2C%20who%20writes,reads%20like%20a%20Baudrillard%20essay., https://vizologi.com/business-strategy-canvas/ssense-business-model-canvas/#:~:text=The%20landscape%20of%20high%2Dend,brands%2C%20alongside%20superior%20customer%20service.

**Google FR** (ai_mode_fallback):
> 19 sitesThe Best Online Stores for Fashion Lovers - smcfashion.com14 mai 2025 — The Best Online Stores for Fashion Lovers. Ever found yourself scrolling endlessly through your phone at 2 AM, hunting for that pe...smcfashion.comFarfetch or Ssense : r/viviennewestwood - Reddit12 oct. 2025 — * Comparison of Farfetch and Ssense. * Vivienne Westwood products on Ssense. * Alternatives to Farfetch for shopping. * Ssense alt...RedditFarfetch, Ssense, what else? : r/luxurypurses - Reddit19 oct. 2024 — Farfetch, Ssense, what else? Sorry, this post was deleted by the person who originally posted it. ... 
> Sources: https://www.ssense.com/en-ae/customer-service, https://www.reddit.com/r/BuyCanadian/comments/1h3fxwf/dont_buy_from_ssense/, https://www.yournextshoes.com/ssense-shipping-return-policy/#:~:text=Countries%20such%20as%20Austria%2C%20Switzerland,did%20SSENSE%20shut%20down%20Polyvore?, https://www.farfetch.com/ca/shopping/men/coats-2/items.aspx#:~:text=Statement%20pieces%20or%20winter%20warmers,S%2C%20M%2C%20XXL, https://www.reddit.com/r/luxurypurses/comments/14ywsv9/is_ssensecom_legit/

---

## Revenue Impact

- **Quebec French-speaking market:** ~7M consumers
- **IAS 60/100** = ~40% of French AI queries failing or degraded
- AI-driven product discovery growing 40%+ YoY -- gap compounds quarterly

## What Fixes This

Bilingual JSON-LD injection + AI-readable product feeds (UCP/ACP) + Headless Agentic Probing to verify.

---
*Generated by Lead Gen Engine | Alex, AI PM -- Montreal (JMSB/Ampliwork)*