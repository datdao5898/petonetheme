# Petone — Shopify theme

Custom Shopify Online Store 2.0 theme for **Petone**, a smart pet-tech store (self-cleaning litter boxes, fountains, feeders…).
Homepage layout is inspired by petsnowy.com, but all branding/content is Petone's own — never copy PetSnowy assets, names or copy.
The owner speaks Vietnamese — reply in Vietnamese; keep theme UI strings / schema labels in English (locales are used for storefront text).

## Brand
- Dark `#060709`, accent green `#53BD8E` (hover `#3FA578`), white `#FFFFFF`, soft surface `#F2F5F3`
- Font: Poppins (Shopify font_picker defaults `poppins_n7` / `poppins_n4`)
- Logo assets: `assets/logo-green.png` (on dark), `assets/logo-dark.png` (on light), `assets/logo-white.png`
- Style: rounded cards (radius 20px), pill buttons, bold tight headings, dark header/footer

## Structure
- `layout/theme.liquid` — CSS variables from theme settings, loads `assets/base.css` + `assets/theme.js`
- `config/settings_schema.json` — global settings (logo, colors, fonts, layout, cards, cart, social)
- `sections/` — homepage: `announcement-bar`, `header`, `hero`, `trust-bar`, `bundle-grid`, `product-tabs`, `brand-story`, `faq`, `footer`, `rich-text`, `custom-liquid`; inner pages: `main-*`, `contact-form`
- `sections/header-group.json`, `sections/footer-group.json` — section groups
- `snippets/` — `product-card`, `price`, `product-badge`, `product-savings`, `icon`, `logo`, `pagination`, `cart-notification`, `social-icons`, `meta-tags`
- `assets/theme.js` — custom elements: `announcement-rotator`, `sticky-header`, `tabs-component`; AJAX add-to-cart for any `form.js-add-form`; qty steppers; reveal-on-scroll
- `templates/*.json` — all OS 2.0 JSON templates (+ `gift_card.liquid`, `customers/*`)

## Conventions
- Every section: `section.settings.padding_top/bottom` → `--pt/--pb` CSS vars on `.section`; background via `bg-white | bg-surface | bg-dark | bg-accent`
- Content width: `.page-width`; headings in `.section-head` with `.eyebrow` + `.h1`
- Product badges come from product tags `badge:<Label>`; savings / % off computed from compare_at_price
- Storefront strings go through `locales/en.default.json` with `| t`
- Custom elements must be `display: block` (already set in base.css)
- No build step — plain Liquid/CSS/JS

## Checks
- `python scripts/validate.py .` — custom validator: schema JSON, Liquid tag balance, translation keys, snippet/asset references, setting ids used vs declared, range/select defaults, template ↔ schema consistency. Must print `OK — no issues`.
- If Shopify CLI is installed: `shopify theme check` and `shopify theme dev --store <store>.myshopify.com`
- `python scripts/build_preview.py . preview.html` — static homepage mock using real CSS/JS (manual HTML mirror; update it when markup changes)

## Deploy
Plan: push to GitHub repo `datdao5898/petonetheme` (private, branch `main` = live, `dev` = staging), then Shopify Admin → Online Store → Themes → Add theme → Connect from GitHub.
`.shopifyignore` excludes `scripts/`, `CLAUDE.md`, `README.md` from CLI pushes.

## Backlog (agreed priority)
1. **App blocks** — add `{ "type": "@app" }` to `main-product` (and render `{% render block %}` for app blocks) so review / installment / upsell apps can be added
2. **Cart drawer** — replace the toast (`snippets/cart-notification.liquid`) with a slide-in cart using the Section Rendering API
3. Collection **filters** (`collection.filters`, Search & Discovery)
4. **Predictive search** in header
5. Product page: color swatches, sold-out variant states, selling plans (subscriptions), pickup availability, Shopify product recommendations, sticky mobile add-to-cart
6. Translations: Vietnamese / Khmer locale files
7. Test on a real store (unpublished theme) and place a test order before publishing
