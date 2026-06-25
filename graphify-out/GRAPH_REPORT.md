# Graph Report - .  (2026-06-25)

## Corpus Check
- Corpus is ~31,597 words - fits in a single context window. You may not need a graph.

## Summary
- 293 nodes · 295 edges · 75 communities (21 shown, 54 thin omitted)
- Extraction: 75% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 72 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Page templates & article layout|Page templates & article layout]]
- [[_COMMUNITY_Theme search (TypeScript)|Theme search (TypeScript)]]
- [[_COMMUNITY_Theme article components & widgets|Theme article components & widgets]]
- [[_COMMUNITY_Head & footer partials|Head & footer partials]]
- [[_COMMUNITY_Photovoltaic experience posts (drafts)|Photovoltaic experience posts (drafts)]]
- [[_COMMUNITY_Theme configuration|Theme configuration]]
- [[_COMMUNITY_Comment system providers|Comment system providers]]
- [[_COMMUNITY_Color scheme controller (TS)|Color scheme controller (TS)]]
- [[_COMMUNITY_Image gallery  PhotoSwipe (TS)|Image gallery / PhotoSwipe (TS)]]
- [[_COMMUNITY_Theme metadata & licensing|Theme metadata & licensing]]
- [[_COMMUNITY_NPM package & Netlify deps|NPM package & Netlify deps]]
- [[_COMMUNITY_Markdown render hooks|Markdown render hooks]]
- [[_COMMUNITY_CICD deploy & theme update|CI/CD deploy & theme update]]
- [[_COMMUNITY_Scrollspy  TOC tracking (TS)|Scrollspy / TOC tracking (TS)]]
- [[_COMMUNITY_JSTS project config|JS/TS project config]]
- [[_COMMUNITY_Media embed shortcodes|Media embed shortcodes]]
- [[_COMMUNITY_Favicon font attribution|Favicon font attribution]]
- [[_COMMUNITY_Color utility (TS)|Color utility (TS)]]
- [[_COMMUNITY_Menu animations (TS)|Menu animations (TS)]]
- [[_COMMUNITY_Netlify CMS|Netlify CMS]]
- [[_COMMUNITY_Theme JS entry point|Theme JS entry point]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]

## God Nodes (most connected - your core abstractions)
1. `Search` - 15 edges
2. `Comments Include Dispatcher` - 12 edges
3. `helper/icon Partial` - 10 edges
4. `StackColorScheme` - 9 edges
5. `Article Partial` - 9 edges
6. `Head Partial` - 9 edges
7. `StackGallery` - 7 edges
8. `Photovoltaic: my experience after 2 months` - 7 edges
9. `search page template` - 6 edges
10. `article-list/compact partial` - 6 edges

## Surprising Connections (you probably didn't know these)
- `article-list/compact partial` --semantically_similar_to--> `article/components/links.html`  [INFERRED] [semantically similar]
  layouts/partials/article-list/compact.html → themes/hugo-theme-stack/layouts/partials/article/components/links.html
- `search page template` --implements--> `Search`  [INFERRED]
  layouts/page/search.html → themes/hugo-theme-stack/layouts/page/search.html
- `Deploy to GitHub Pages workflow` --references--> `Hugo Modules theme loading`  [INFERRED]
  .github/workflows/deploy.yml → README.md
- `Hugo Theme Stack Starter Template` --references--> `Deploy to GitHub Pages workflow`  [INFERRED]
  README.md → .github/workflows/deploy.yml
- `Hugo Theme Stack Starter Template` --references--> `Update theme workflow (cron)`  [INFERRED]
  README.md → .github/workflows/update-theme.yml

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Hugo module theme + GitHub Pages deploy pipeline** — readme_hugo_modules, deploy_deploy_to_github_pages, update_theme_update_theme [INFERRED 0.85]
- **Photovoltaic experience article series** — photovoltaic_rex_after_2_months_article, photovoltaic_rex_after_9_months_part1_article, photovoltaic_rex_after_9_months_part2_article, photovoltaic_rex_after_a_year_article, calculate_photovoltaic_roi_article [EXTRACTED 1.00]
- **Article-list templates sharing image/header partials** — article_list_compact, article_list_default, article_list_helper_image, article_list_header_from_article_list [EXTRACTED 1.00]
- **Article Rendering Pipeline** — article_article, article_components_header, article_components_content, article_components_footer [EXTRACTED 1.00]
- **Site Owner Custom Theme Overrides** — contact_form_feature, donate_feature, substack_feature, image_conversion_feature [INFERRED 0.75]
- **Theme i18n translations** — i18n_ar, i18n_be, i18n_bg, i18n_bn, i18n_ca, i18n_cs, i18n_de, i18n_el, i18n_en [INFERRED 0.75]
- **Theme i18n translations (es-zh)** — i18n_es, i18n_fa, i18n_fr, i18n_hi, i18n_hu, i18n_id, i18n_it, i18n_ja, i18n_ko, i18n_nl, i18n_oc, i18n_pl, i18n_pt_br, i18n_pt_pt, i18n_ru, i18n_sk, i18n_th, i18n_tr, i18n_uk, i18n_vi, i18n_zh_cn, i18n_zh_hk, i18n_zh_tw [EXTRACTED 1.00]
- **Markdown render hook set** — _markup_render_link, _markup_render_image, _markup_render_heading, _markup_render_codeblock_mermaid [INFERRED 0.85]
- **Article list rendering variants** — article_list_compact, article_list_default, article_list_tile [INFERRED 0.85]
- **Article component partial set** — components_header, components_content, components_footer, components_details, article_article [EXTRACTED 0.85]
- **Optional article feature components** — components_math, components_mermaid, components_photoswipe, components_related_content, components_tags [INFERRED 0.75]
- **Comment system providers** — provider_beaudar, provider_cactus, provider_cusdis, provider_disqus, provider_disqusjs, provider_giscus, provider_gitalk, provider_remark42, provider_twikoo, provider_utterances, provider_vssue, provider_waline [EXTRACTED 1.00]
- **Head subsystem partials** — head_head, head_style, head_script, head_colorscheme, head_custom, opengraph_include [INFERRED 0.75]
- **OpenGraph provider dispatch** — opengraph_include, provider_base, provider_twitter [EXTRACTED 1.00]
- **Reusable helper utility partials** — helper_icon, helper_image, helper_external, helper_color_from_str, helper_paginator [INFERRED 0.75]
- **Sidebar widgets** — widget_archives, widget_categories, widget_search, widget_tag_cloud, widget_toc [INFERRED 0.85]
- **Media embed shortcodes** — shortcodes_bilibili, shortcodes_tencent, shortcodes_video, shortcodes_youtube [INFERRED 0.85]

## Communities (75 total, 54 thin omitted)

### Community 0 - "Page templates & article layout"
Cohesion: 0.11
Nodes (26): 404 not-found page template, 404 search-keyword recovery from URL, archives template (group by year), list template (sections/paginated), Article Partial, Article Content Component, Article Footer Component, Article Math Component (+18 more)

### Community 1 - "Theme search (TypeScript)"
Cohesion: 0.15
Nodes (6): match, pageData, replaceHTMLEnt(), Search, tagsToReplace, Window

### Community 2 - "Theme article components & widgets"
Cohesion: 0.11
Nodes (20): Article Details Component, Article Details (from list) Component, Article Header Component, Article Header (from list) Component, Category taxonomy cloud, Pagination, Posts grouped by year, Site search form (+12 more)

### Community 3 - "Head & footer partials"
Cohesion: 0.13
Nodes (20): Canonical URL Override, footer/components/custom-font.html, footer/components/script.html, Hugo asset pipeline (js.Build/toCSS/fingerprint), OpenGraph / social metadata, data/description Partial, data/title Partial, footer/components/script Partial (+12 more)

### Community 4 - "Photovoltaic experience posts (drafts)"
Cohesion: 0.16
Nodes (18): Un meilleur calcul de la rentabilite du photovoltaique, HP/HC self-consumption savings recalculation, Recalculated profitability date (2028-2029), Photovoltaic: my experience after 2 months, PV installation (8 recycled 190Wc panels, APSystems QS1), PVGIS sun exposure simulation, Self-consumption priority (no grid resale at ground level), Robin Emley MK2 PV solar router (+10 more)

### Community 5 - "Theme configuration"
Cohesion: 0.18
Nodes (13): Categories archetype, Tags archetype, Color scheme toggle (auto/light/dark), Comment providers (disqus, utterances, giscus, waline, etc.), Image processing (cover, content), Menus (main, social), Multilingual languages config (en, zh-cn, ar), Sidebar (avatar, subtitle, emoji) (+5 more)

### Community 6 - "Comment system providers"
Cohesion: 0.17
Nodes (13): Comments Include Dispatcher, Beaudar Comments Provider, Cactus Comments Provider, Cusdis Comments Provider, Disqus Comments Provider, DisqusJS Comments Provider, Giscus Comments Provider, Gitalk Comments Provider (+5 more)

### Community 8 - "Image gallery / PhotoSwipe (TS)"
Cohesion: 0.29
Nodes (3): PhotoSwipeItem, StackGallery, Window

### Community 9 - "Theme metadata & licensing"
Cohesion: 0.22
Nodes (9): Default archetype, exampleSite README, FUNDING configuration, Bug Report issue template, Issue template config, Card-style blogger theme, GPL v3.0 license, Hugo Theme Stack (+1 more)

### Community 10 - "NPM package & Netlify deps"
Cohesion: 0.25
Nodes (7): dependencies, @netlify/functions, devDependencies, netlify-cli, @types/node, scripts, netlify

### Community 11 - "Markdown render hooks"
Cohesion: 0.29
Nodes (6): image-converter partial (webp/jpg conversion), render-heading hook template, render-image hook template (responsive srcset), render-image-webp hook template, render-link hook template (.md relref handling), Markdown Render Hooks

### Community 12 - "CI/CD deploy & theme update"
Cohesion: 0.38
Nodes (7): Deploy to GitHub Pages workflow, Hugo build step (hugo --minify --gc), Hugo Modules theme loading, Hugo Theme Stack Starter Template, Prettier go-template HTML formatter setup, Hugo module theme update (hugo mod get), Update theme workflow (cron)

### Community 13 - "Scrollspy / TOC tracking (TS)"
Cohesion: 0.43
Nodes (5): buildIdToNavigationElementMap(), computeOffsets(), debounced(), IdToElementMap, setupScrollspy()

### Community 14 - "JS/TS project config"
Cohesion: 0.40
Nodes (4): compilerOptions, baseUrl, paths, *

### Community 15 - "Media embed shortcodes"
Cohesion: 0.40
Nodes (5): Responsive video embed, Bilibili shortcode, Tencent video shortcode, HTML5 video shortcode, YouTube shortcode

### Community 16 - "Favicon font attribution"
Cohesion: 0.60
Nodes (5): Akronim Font, Favicon Attribution (about-dark-over-light), SIL Open Font License 1.1, Favicon Attribution (about-light-over-dark), Favicon Attribution (dark-about)

### Community 18 - "Menu animations (TS)"
Cohesion: 0.83
Nodes (3): slideDown(), slideToggle(), slideUp()

### Community 19 - "Netlify CMS"
Cohesion: 1.00
Nodes (3): Netlify CMS Config, Netlify CMS Admin Page, Netlify CMS Content Management

## Ambiguous Edges - Review These
- `Pagination` → `sidebar/right.html`  [AMBIGUOUS]
  themes/hugo-theme-stack/layouts/partials/sidebar/right.html · relation: conceptually_related_to

## Knowledge Gaps
- **134 isolated node(s):** `baseUrl`, `*`, `init-prettier-golang-html-formatter.sh script`, `netlify`, `@netlify/functions` (+129 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **54 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Pagination` and `sidebar/right.html`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `helper/image Partial` connect `Head & footer partials` to `Page templates & article layout`, `Theme article components & widgets`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `Article Header Component` connect `Theme article components & widgets` to `Page templates & article layout`, `Head & footer partials`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **What connects `baseUrl`, `*`, `init-prettier-golang-html-formatter.sh script` to the rest of the system?**
  _136 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Page templates & article layout` be split into smaller, more focused modules?**
  _Cohesion score 0.11330049261083744 - nodes in this community are weakly interconnected._
- **Should `Theme search (TypeScript)` be split into smaller, more focused modules?**
  _Cohesion score 0.14624505928853754 - nodes in this community are weakly interconnected._
- **Should `Theme article components & widgets` be split into smaller, more focused modules?**
  _Cohesion score 0.11428571428571428 - nodes in this community are weakly interconnected._