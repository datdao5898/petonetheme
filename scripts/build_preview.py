import base64, sys
T = sys.argv[1]; OUT = sys.argv[2]
css = open(f'{T}/assets/base.css').read()
js = open(f'{T}/assets/theme.js').read()
logo = base64.b64encode(open(f'{T}/assets/logo-green.png','rb').read()).decode()
logo_img = f'<img class="logo__img" src="data:image/png;base64,{logo}" alt="Petone" width="648" height="152">'
def icon(name):
    import re
    s = open(f'{T}/snippets/icon.liquid').read()
    m = re.search(r"when '"+re.escape(name)+r"' -%}\s*(<svg.*?</svg>)", s, re.S)
    return m.group(1)
# product illustrations
def prod(kind, bg='#ffffff'):
    shapes = {
     'litter': '<rect x="70" y="120" width="260" height="190" rx="40" fill="#e9eeeb"/><path d="M90 180a110 110 0 0 1 220 0v20H90z" fill="#f7f9f8" stroke="#d5ddd9" stroke-width="3"/><circle cx="200" cy="215" r="48" fill="#060709"/><rect x="150" y="285" width="100" height="10" rx="5" fill="#53BD8E"/>',
     'fountain': '<ellipse cx="200" cy="300" rx="120" ry="18" fill="#e3e9e6"/><path d="M110 170h180l-20 130H130z" fill="#f7f9f8" stroke="#d5ddd9" stroke-width="3"/><ellipse cx="200" cy="170" rx="90" ry="20" fill="#bfe8d5"/><path d="M200 165c0-30 0-55 0-70" stroke="#53BD8E" stroke-width="10" stroke-linecap="round"/><circle cx="200" cy="90" r="10" fill="#53BD8E"/>',
     'feeder': '<rect x="130" y="80" width="140" height="190" rx="30" fill="#f7f9f8" stroke="#d5ddd9" stroke-width="3"/><rect x="150" y="100" width="100" height="90" rx="16" fill="#e9eeeb"/><path d="M110 270h180v20a20 20 0 0 1-20 20H130a20 20 0 0 1-20-20z" fill="#060709"/><circle cx="200" cy="225" r="12" fill="#53BD8E"/>',
     'purifier': '<rect x="135" y="70" width="130" height="240" rx="40" fill="#f7f9f8" stroke="#d5ddd9" stroke-width="3"/><g fill="#d5ddd9">'+''.join(f'<rect x="160" y="{110+i*22}" width="80" height="8" rx="4"/>' for i in range(6))+'</g><circle cx="200" cy="90" r="8" fill="#53BD8E"/>',
     'vacuum': '<rect x="185" y="60" width="30" height="190" rx="15" fill="#060709"/><rect x="130" y="240" width="140" height="50" rx="22" fill="#f7f9f8" stroke="#d5ddd9" stroke-width="3"/><circle cx="200" cy="120" r="34" fill="#f7f9f8" stroke="#d5ddd9" stroke-width="3"/><circle cx="200" cy="120" r="12" fill="#53BD8E"/>',
     'dryer': '<rect x="90" y="90" width="220" height="200" rx="40" fill="#f7f9f8" stroke="#d5ddd9" stroke-width="3"/><rect x="120" y="120" width="160" height="110" rx="24" fill="#cfe9dc"/><circle cx="200" cy="260" r="9" fill="#060709"/>',
    }
    return f'<svg class="product-card__img" viewBox="0 0 400 380" style="padding:0;background:{bg}">{shapes[kind]}</svg>'
def bundle_img(kinds, bg):
    inner = ''
    n=len(kinds)
    for i,k in enumerate(kinds):
        x = (i - (n-1)/2) * 120
        svg = prod(k).replace('<svg class="product-card__img" viewBox="0 0 400 380" style="padding:0;background:#ffffff">','').replace('</svg>','')
        inner += f'<g transform="translate({200+x-110},{60}) scale(.55)">{svg}</g>'
    return f'<svg viewBox="0 0 400 400" style="background:{bg}"><circle cx="200" cy="200" r="150" fill="#ffffff" opacity=".7"/>{inner}</svg>'

hero_bg = '''<svg viewBox="0 0 1600 800" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%">
<defs><radialGradient id="g" cx="72%" cy="45%" r="55%"><stop offset="0" stop-color="#53BD8E" stop-opacity=".55"/><stop offset=".55" stop-color="#1c3b2f" stop-opacity=".6"/><stop offset="1" stop-color="#060709"/></radialGradient></defs>
<rect width="1600" height="800" fill="#060709"/><rect width="1600" height="800" fill="url(#g)"/>
<g transform="translate(1020,170) scale(1.25)" opacity=".95"><rect x="0" y="120" width="360" height="270" rx="60" fill="#e9eeeb"/><path d="M28 210a152 152 0 0 1 304 0v30H28z" fill="#f7f9f8"/><circle cx="180" cy="262" r="70" fill="#060709"/><rect x="110" y="360" width="140" height="12" rx="6" fill="#53BD8E"/></g>
<g fill="#53BD8E" opacity=".08" transform="translate(120,520) scale(9)"><ellipse cx="6" cy="10" rx="2.2" ry="2.8"/><ellipse cx="18" cy="10" rx="2.2" ry="2.8"/><ellipse cx="9.5" cy="5.5" rx="2.2" ry="2.8"/><ellipse cx="14.5" cy="5.5" rx="2.2" ry="2.8"/><path d="M12 11c-3 0-6 4.5-6 7 0 1.8 1.5 2.5 3 2.2 1.2-.2 2-.7 3-.7s1.8.5 3 .7c1.5.3 3-.4 3-2.2 0-2.5-3-7-6-7Z"/></g>
</svg>'''
story1 = '<svg viewBox="0 0 900 600" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="s1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a4a3d"/><stop offset="1" stop-color="#0d1512"/></linearGradient></defs><rect width="900" height="600" fill="url(#s1)"/><circle cx="640" cy="220" r="170" fill="#53BD8E" opacity=".25"/><g transform="translate(520,90) scale(.9)"><rect x="0" y="120" width="260" height="190" rx="40" fill="#e9eeeb"/><path d="M20 180a110 110 0 0 1 220 0v20H20z" fill="#f7f9f8"/><circle cx="130" cy="215" r="48" fill="#060709"/></g></svg>'
story2 = '<svg viewBox="0 0 600 600" preserveAspectRatio="xMidYMid slice"><rect width="600" height="600" fill="#1a1f22"/><circle cx="300" cy="230" r="150" fill="#53BD8E" opacity=".18"/><g fill="#53BD8E" opacity=".5" transform="translate(220,140) scale(7)"><ellipse cx="6" cy="10" rx="2.2" ry="2.8"/><ellipse cx="18" cy="10" rx="2.2" ry="2.8"/><ellipse cx="9.5" cy="5.5" rx="2.2" ry="2.8"/><ellipse cx="14.5" cy="5.5" rx="2.2" ry="2.8"/><path d="M12 11c-3 0-6 4.5-6 7 0 1.8 1.5 2.5 3 2.2 1.2-.2 2-.7 3-.7s1.8.5 3 .7c1.5.3 3-.4 3-2.2 0-2.5-3-7-6-7Z"/></g></svg>'

menu = ['Fall Sale','Collections','Accessories','Why Petone','Contact']
nav = ''.join(f'<li class="header__menu-item{" has-dropdown" if m=="Collections" else ""}"><a href="#" class="header__link">{m}{icon("chevron-down") if m=="Collections" else ""}</a>' + ('<div class="header__dropdown"><ul><li><a href="#">Litter boxes</a></li><li><a href="#">Fountains</a></li><li><a href="#">Feeders</a></li></ul></div>' if m=='Collections' else '') + '</li>' for m in menu)
drawer = ''.join(f'<li><a href="#">{m}</a></li>' for m in menu)

bundles = [('Hands-free','The Complete Hands-Free Home','Litter box + Fountain + Feeder','Save 39%',['fountain','litter','feeder'],'$899','$1,467'),
           ('Odor control','Zero Odor Combo','Litter box + Air purifier','Save 39%',['litter','purifier'],'$699','$1,147'),
           ('Hydration','Fresh Water Set','Litter box + Fountain','Save 34%',['litter','fountain'],'$629','$953'),
           ('Starter','The Fresh Set','Fountain + Filters','Save 39%',['fountain'],'$89','$146')]
bhtml = ''
for lab,t,inc,badge,k,p,c in bundles:
    bhtml += f'''<article class="bundle-card"><div class="bundle-card__top"><span class="bundle-card__label">{lab}</span><span class="badge badge--sale">{badge}</span></div>
<a class="bundle-card__media" href="#">{bundle_img(k,'#eef3f0')}</a>
<div class="bundle-card__body"><h3 class="bundle-card__title">{t}</h3><p class="bundle-card__includes">{inc}</p>
<div class="price price--on-sale"><span class="price__current">{p}</span><s class="price__compare">{c}</s></div>
<div class="bundle-card__actions"><a href="#" class="link-underline">See details</a><form class="js-add-form"><button type="button" class="button button--small">Add to cart</button></form></div></div></article>'''
prods = [('litter','SNOW+ Self-Cleaning Litter Box','Top 1','Save $170','-22%','$599','$769'),
         ('fountain','OilClear A.I Smart Fountain','New','Up to $50 off','-30%','$119','$169'),
         ('purifier','Pet Air Purifier Pro','Just Launched','Save $70','-25%','$209','$279'),
         ('vacuum','VacPro Wireless Pet Vacuum','Hot','Up to $40 off','-18%','$179','$219'),
         ('feeder','SmartBowl Auto Feeder','New','Save $30','-20%','$119','$149'),
         ('dryer','AirDry Pet Grooming Box','Top 1','Save $90','-15%','$499','$589')]
phtml = ''
for k,t,tag,sav,pct,p,c in prods:
    phtml += f'''<div class="carousel__slide"><div class="product-card"><a href="#" class="product-card__media"><div class="product-card__badges"><span class="badge badge--tag">{tag}</span><span class="badge badge--sale">{pct}</span></div>{prod(k)}</a>
<div class="product-card__info"><h3 class="product-card__title"><a href="#">{t}</a></h3><div class="product-card__savings"><span class="savings">{sav}</span></div>
<div class="price price--on-sale"><span class="price__current">{p}</span><s class="price__compare">{c}</s></div><a href="#" class="button button--small button--dark product-card__btn">Shop now</a></div></div></div>'''
faqs = [('What is Petone?','Petone is a smart pet care brand creating connected products — self-cleaning litter boxes, water fountains, feeders and grooming tools — that make daily pet care easier and more hygienic.'),
        ('Which pets are Petone products designed for?','Most of our products are designed for cats and small to medium dogs.'),
        ('How long does shipping take?','Orders are usually processed within 1–2 business days.'),
        ('What warranty do you offer?','All Petone devices include a manufacturer warranty.'),
        ('Can I return a product?','Yes. You can try Petone risk-free for 30 days.')]
fhtml = ''.join(f'<details class="faq-item"{" open" if i==0 else ""}><summary><span>{q}</span><span class="faq-item__icon">{icon("plus")}</span></summary><div class="faq-item__answer rte"><p>{a}</p></div></details>' for i,(q,a) in enumerate(faqs))
trust = [('trial','30-day trial','Risk-free returns'),('shipping','Free shipping','On orders over $49'),('warranty','Up to 2-year warranty','Peace of mind included'),('payment','Pay later','Flexible installments')]
thtml = ''.join(f'<li class="trust-item"><span class="trust-item__icon">{icon(i)}</span><span><strong class="trust-item__title">{a}</strong><span class="trust-item__text">{b}</span></span></li>' for i,a,b in trust)
social = ''.join(f'<li><a href="#">{icon(s)}</a></li>' for s in ['facebook','instagram','tiktok','youtube'])

# Hero slideshow (mirror of sections/hero.liquid)
hero_slides = [
  ('left', 'Smart pet tech for modern homes', 'Smarter care. <em>Happier pets.</em>', 'Self-cleaning litter boxes, smart fountains and feeders that take care of the daily chores — so you can enjoy more time with your pet.', 'Shop the sale', 'Why Petone'),
  ('left', 'Self-cleaning litter box', 'Scoop-free. <em>Odor-free.</em>', 'Automatic cleaning, sealed waste drawer and app alerts — fresh every day without lifting a finger.', 'Shop litter boxes', ''),
  ('center', 'Smart fountains', 'Fresh water, <em>all day.</em>', 'Quiet pumps and triple filtration keep your pet hydrated and healthy.', 'Shop fountains', 'Learn more'),
]
def _slide(i, s):
    pos, eb, h, sub, b1, b2 = s
    tag = 'h1' if i == 0 else 'h2'
    btn2 = f'<a href="#" class="button button--large button--ghost">{b2}</a>' if b2 else ''
    attrs = ' is-active"' if i == 0 else '" aria-hidden="true" inert'
    return (f'<div class="hero__slide hero--align-{pos}{attrs} role="group" aria-roledescription="slide" data-slide><div class="hero__media">{hero_bg}</div>'
            f'<div class="hero__content page-width"><div class="hero__text"><p class="eyebrow">{icon("paw")} {eb}</p><{tag} class="hero__heading h-display">{h}</{tag}><p class="hero__sub">{sub}</p>'
            f'<div class="button-row"><a href="#" class="button button--large">{b1} {icon("arrow-right")}</a>{btn2}</div></div></div></div>')
hero_dots = ''.join(f'<button type="button" class="hero__dot{" is-active" if i == 0 else ""}" data-slide-to="{i}"><span></span></button>' for i in range(len(hero_slides)))
hero_html = ('<hero-slider class="hero hero--large hero--has-controls" style="--overlay:.35;--slide-speed:6s" data-autoplay data-speed="6" role="region" aria-roledescription="carousel">'
  '<div class="hero__slides">' + ''.join(_slide(i, s) for i, s in enumerate(hero_slides)) +
  f'<div class="hero__controls"><button type="button" class="hero__arrow" data-slide-prev>{icon("chevron-left")}</button><div class="hero__dots">{hero_dots}</div><button type="button" class="hero__arrow" data-slide-next>{icon("chevron-right")}</button></div></div>'
  f'<div class="hero__extras page-width"><div class="hero__promo"><span class="badge badge--accent">Fall Sale</span><p class="hero__promo-heading">Settle into fall. Keep it fresh.</p><p class="hero__promo-amount">Save up to $400</p><a href="#" class="hero__promo-link">Shop bundles {icon("arrow-right")}</a></div></div>'
  '</hero-slider>')

# Image sections (mirrors of spotlight-stack / bento-gallery / shop-the-look)
def scene(kind, c1, c2, x=62, scale=1.6, cls=''):
    inner = prod(kind).split('>', 1)[1].rsplit('</svg>', 1)[0]
    return (f'<svg class="{cls}" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%">'
            f'<rect width="1600" height="900" fill="{c2}"/><circle cx="{x*16}" cy="430" r="520" fill="{c1}" opacity=".55"/>'
            f'<g transform="translate({x*16-200*scale},{450-200*scale}) scale({scale})">{inner}</g></svg>')

spots = [('litter', 'dark', 'left', 'Just launched', 'Petone Smart Series', 'Self-cleaning <em>litter box</em>', 'Save $120 · Limited-time deal', '#2f6b52', '#0c1411', 70),
         ('fountain', 'light', 'right', 'New', 'Petone Hydra', 'Smart <em>water fountain</em>', 'Up to $40 off · Exclusive savings', '#cfe9dc', '#9fb8ad', 30),
         ('feeder', 'accent', 'left', 'Best seller', 'Petone Feast', 'App-controlled <em>feeder</em>', 'Save $60 · This week only', '#53BD8E', '#1d3a2e', 70)]
spot_cards = ''
for i, (k, sch, side, badge, kick, h, offer, c1, c2, x) in enumerate(spots):
    b1 = 'button--dark' if sch == 'accent' else 'button--accent'
    spot_cards += (f'<article class="spotlight spotlight--{sch} spotlight--text-{side}" data-stack-card><div class="spotlight__media">{scene(k, c1, c2, x, 1.7, "spotlight__img")}</div>'
                   f'<span class="spotlight__index" aria-hidden="true">0{i+1}</span><div class="spotlight__content"><span class="badge badge--accent">{badge}</span><p class="spotlight__kicker">{kick}</p>'
                   f'<h3 class="spotlight__heading">{h}</h3><p class="spotlight__offer">{offer}</p><div class="button-row"><a href="#" class="button {b1}">Shop now {icon("arrow-right")}</a>'
                   f'<a href="#" class="button spotlight__ghost">{icon("play")} Watch demo</a></div></div></article>')
spot_html = ('<section class="section spotlight-stack bg-surface" style="--pt:80px;--pb:80px"><div class="page-width"><div class="section-head"><div><p class="eyebrow">In the spotlight</p>'
             '<h2 class="h1">New tech for <em>happier homes</em></h2></div></div></div>'
             f'<stack-cards class="spotlight-stack__list page-width">{spot_cards}</stack-cards></section>')

tiles = [('large', 'image', 'litter', 'Litter care', '', 'Scoop-free <em>mornings</em>', '#2f6b52', '#0c1411'),
         ('small', 'accent', None, 'Odor control', '99%', 'fewer odors at home', '', ''),
         ('tall', 'image', 'fountain', 'Hydration', '', 'Fresh water, all day', '#cfe9dc', '#7f9a8e'),
         ('small', 'dark', None, 'Peace of mind', '24/7', 'App alerts anywhere', '', ''),
         ('wide', 'image', 'feeder', 'Feeding', '', 'Meals right on schedule', '#e3d2bb', '#a98f6f'),
         ('wide', 'image', 'dryer', 'Grooming', '', 'Less fur, <em>more cuddles</em>', '#53BD8E', '#183126')]
tile_html = ''
for size, style, k, label, big, h, c1, c2 in tiles:
    media = f'<div class="bento-tile__media">{scene(k, c1, c2, 50, 1.9)}</div>' if style == 'image' else ''
    bigs = f'<span class="bento-tile__big">{big}</span>' if big else ''
    arrow = f'<span class="bento-tile__arrow" aria-hidden="true">{icon("arrow-right")}</span>' if style == 'image' else ''
    tag = 'a href="#"' if style == 'image' else 'div'
    end = 'a' if style == 'image' else 'div'
    tile_html += (f'<{tag} class="bento-tile bento-tile--{size} bento-tile--{style}">{media}<div class="bento-tile__body"><span class="bento-tile__label">{label}</span>{bigs}'
                  f'<h3 class="bento-tile__heading">{h}</h3></div>{arrow}</{end}>')
bento_html = ('<section class="section bento bg-white" style="--pt:80px;--pb:80px"><div class="page-width"><div class="section-head"><div><p class="eyebrow">Life with Petone</p>'
              f'<h2 class="h1">Made for the way <em>pets live</em></h2></div><a href="#" class="link-arrow">Explore all {icon("arrow-right")}</a></div>'
              f'<div class="bento__grid">{tile_html}</div></div></section>')

look_items = [('litter', 'SNOW+ Self-Cleaning Litter Box', '$599', '$769', 68, 62), ('fountain', 'Hydra Smart Fountain', '$89', '', 30, 70), ('feeder', 'Feast App Feeder', '$129', '$159', 46, 40)]
look_svg = ('<svg viewBox="0 0 1000 800" preserveAspectRatio="xMidYMid slice"><rect width="1000" height="800" fill="#1d2a24"/><rect y="520" width="1000" height="280" fill="#2b3a33"/>'
            '<circle cx="760" cy="200" r="260" fill="#53BD8E" opacity=".18"/>'
            + ''.join(f'<g transform="translate({x*10-110},{y*8-110}) scale(.55)">{prod(k).split(">", 1)[1].rsplit("</svg>", 1)[0]}</g>' for k, _, _, _, x, y in look_items) + '</svg>')
dots = ''.join(f'<button type="button" class="look__dot{" is-active" if i == 0 else ""}" style="--x:{x}%;--y:{y}%" data-look-dot="{i}"><span class="look__dot-num">{i+1}</span>'
               f'<span class="look__dot-tip{" look__dot-tip--left" if x > 60 else ""}">{t}</span></button>' for i, (k, t, p, c, x, y) in enumerate(look_items))
items = ''.join(f'<li class="look-item{" is-active" if i == 0 else ""}" data-look-item="{i}"><a href="#" class="look-item__link"><span class="look-item__num">{i+1}</span>'
                f'<span class="look-item__media">{prod(k)}</span><span class="look-item__info"><span class="look-item__title">{t}</span>'
                f'<div class="price{" price--on-sale" if c else ""}"><span class="price__current">{p}</span>{f"<s class=price__compare>{c}</s>" if c else ""}</div></span>'
                f'<span class="look-item__arrow">{icon("arrow-right")}</span></a></li>' for i, (k, t, p, c, x, y) in enumerate(look_items))
look_html = ('<section class="section look bg-dark" style="--pt:80px;--pb:80px"><look-hotspots class="look__layout look__layout--image-left page-width">'
             f'<div class="look__stage"><div class="look__media">{look_svg}</div>{dots}</div>'
             '<div class="look__panel"><p class="eyebrow">Shop the look</p><h2 class="h1">A smarter corner <em>for every pet</em></h2><p class="look__text">Tap the dots to see what makes this setup tick.</p>'
             f'<ol class="look__list scroller" role="list">{items}</ol><a href="#" class="button button--accent look__cta">Shop the full setup {icon("arrow-right")}</a></div></look-hotspots></section>')

html = f'''<!doctype html><html class="no-js" lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Petone — preview</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap">
<style>:root{{--color-dark:#060709;--color-dark-rgb:6,7,9;--color-accent:#53BD8E;--color-accent-rgb:83,189,142;--color-accent-hover:#3FA578;--color-bg:#fff;--color-surface:#F2F5F3;--color-text:#060709;--color-text-rgb:6,7,9;--color-sale:#53BD8E;--font-heading:'Be Vietnam Pro',sans-serif;--font-heading-weight:700;--font-body:'Be Vietnam Pro',sans-serif;--font-body-weight:400;--font-body-weight-bold:700;--heading-scale:1;--page-width:1360px;--radius:20px;--radius-btn:40px;--logo-width:130px}}
{css}</style>
<script>document.documentElement.className='js';window.theme={{cartType:'notification',routes:{{cart:'/cart',cartAdd:'/cart/add'}},strings:{{}}}};</script></head><body>
<div class="announcement scheme-accent"><div class="page-width announcement__inner"><announcement-rotator class="announcement__track" data-speed="5"><p class="announcement__msg is-active"><strong>Save up to 40%</strong> · Fall Sale · Smart care for happier pets</p><p class="announcement__msg">Free shipping on orders over $49 · 30-day risk-free trial</p></announcement-rotator></div></div>
<div class="shopify-section section-header"><sticky-header class="header-wrapper header-wrapper--framed scheme-dark header-wrapper--sticky header-wrapper--overlay"><div class="header-bar"><header class="header page-width">
<details class="menu-drawer"><summary class="header__icon header__icon--menu"><span class="icon-open">{icon("menu")}</span><span class="icon-close">{icon("close")}</span></summary><div class="menu-drawer__panel"><nav><ul class="menu-drawer__list" role="list">{drawer}</ul></nav><div class="menu-drawer__promo"><p><strong>Fall Sale</strong> — save up to 40% on smart pet care.</p></div><ul class="social-icons" role="list">{social}</ul></div></details>
<a href="#" class="header__logo logo">{logo_img}</a>
<nav class="header__nav"><ul class="header__menu" role="list">{nav}</ul></nav>
<div class="header__icons"><details class="header-search"><summary class="header__icon">{icon("search")}</summary><div class="header-search__panel"><form class="search-form page-width"><input type="search" placeholder="Search products"><button class="button button--small">Search</button></form></div></details>
<a href="#" class="header__icon">{icon("account")}</a><a href="#" class="header__icon header__icon--cart">{icon("cart")}<span class="cart-count" data-cart-count>2</span></a><a href="#" class="button button--small header__cta">Shop the sale</a></div>
</header></div></sticky-header></div>
<main id="MainContent">
<div class="shopify-section section-hero">{hero_html}</div>
<section class="section trust-bar bg-white" style="--pt:28px;--pb:28px"><div class="page-width"><ul class="trust-bar__list" role="list">{thtml}</ul></div></section>
<section class="section bundles bg-white" style="--pt:80px;--pb:80px"><div class="page-width"><div class="section-head"><div><p class="eyebrow">Bundle &amp; save</p><h2 class="h1">Choose your pet care bundle</h2><p class="section-head__text">Hand-picked combos that work better together — and cost less.</p></div><a href="#" class="link-arrow">View all bundles {icon("arrow-right")}</a></div>
<div class="bundles__grid scroller" style="--cols:4">{bhtml}</div></div></section>
<section class="section product-tabs bg-surface" style="--pt:80px;--pb:80px"><tabs-component class="page-width"><div class="section-head"><div><p class="eyebrow">Collections</p><h2 class="h1">Smart care for every routine</h2></div><div class="carousel-arrows"><button class="carousel-arrow" data-scroll="prev">{icon("chevron-left")}</button><button class="carousel-arrow" data-scroll="next">{icon("chevron-right")}</button></div></div>
<div class="tabs" role="tablist"><button role="tab" class="tab is-active" aria-selected="true">Best sellers</button><button role="tab" class="tab" aria-selected="false">Litter boxes</button><button role="tab" class="tab" aria-selected="false">Fountains</button><button role="tab" class="tab" aria-selected="false">Feeders</button></div>
<div class="tab-panel is-active" role="tabpanel"><div class="carousel scroller" data-carousel>{phtml}</div></div>
<div class="tab-panel" role="tabpanel" hidden><div class="carousel scroller" data-carousel>{phtml}</div></div><div class="tab-panel" role="tabpanel" hidden><div class="carousel scroller" data-carousel>{phtml}</div></div><div class="tab-panel" role="tabpanel" hidden><div class="carousel scroller" data-carousel>{phtml}</div></div>
</tabs-component></section>
{spot_html}
{bento_html}
<section class="section brand-story bg-dark" style="--pt:88px;--pb:88px"><div class="page-width"><div class="section-head section-head--center"><div><p class="eyebrow">Why Petone</p><h2 class="h1">Smart pet tech, made with love</h2><p class="section-head__text">Designed by pet parents and engineers to make everyday care effortless, hygienic and safe.</p></div></div>
<div class="stats"><div class="stat"><span class="stat__value">50,000+</span><span class="stat__label">Happy pets</span></div><div class="stat"><span class="stat__value">4.8★</span><span class="stat__label">Average rating</span></div><div class="stat"><span class="stat__value">2-year</span><span class="stat__label">Warranty</span></div><div class="stat"><span class="stat__value">24/7</span><span class="stat__label">Pet parent support</span></div></div>
<div class="story-grid story-grid--wide-left"><article class="story-panel"><div class="story-panel__media">{story1}</div><a class="story-panel__play" href="#">{icon("play")}</a><div class="story-panel__content"><p class="eyebrow">Our story</p><h3 class="h2">Built for pets. Trusted by families.</h3><div class="rte"><p>From smart litter boxes to filtered fountains, every Petone product is tested for safety, quietness and durability.</p></div><a href="#" class="button button--accent">Learn more {icon("arrow-right")}</a></div></article>
<article class="story-panel"><div class="story-panel__media">{story2}</div><div class="story-panel__content"><p class="eyebrow">Partner with us</p><h3 class="h2">Creators &amp; media</h3><div class="rte"><p>Love pets and tech? Join the Petone partner program and grow with us.</p></div><a href="#" class="button button--white">Partner with us {icon("arrow-right")}</a></div></article></div></div></section>
{look_html}
<section class="section faq bg-white" style="--pt:88px;--pb:88px"><div class="page-width faq__inner"><div class="faq__intro"><p class="eyebrow">FAQ</p><h2 class="h1">Everything about Petone</h2><div class="rte"><p>Can't find what you're looking for? Our pet parent support team is happy to help.</p></div><a href="#" class="button button--dark">Contact us</a></div><div class="faq__list">{fhtml}</div></div></section>
</main>
<footer class="footer"><div class="page-width"><div class="footer__top"><div class="footer__brand"><a href="#" class="logo footer__logo">{logo_img}</a><div class="footer__about rte"><p>Smart pet tech for modern homes. Less chores, more cuddles.</p></div><ul class="social-icons" role="list">{social}</ul></div>
<div class="footer__cols" style="--cols:3"><div class="footer__col"><h3 class="footer__heading">Information</h3><ul class="footer__links" role="list"><li><a href="#">Return policy</a></li><li><a href="#">Shipping</a></li><li><a href="#">Warranty</a></li><li><a href="#">FAQ</a></li><li><a href="#">Blog</a></li></ul></div>
<div class="footer__col"><h3 class="footer__heading">Company</h3><ul class="footer__links" role="list"><li><a href="#">Why Petone</a></li><li><a href="#">Partner with us</a></li><li><a href="#">Privacy</a></li></ul></div>
<div class="footer__col"><h3 class="footer__heading">Customer service</h3><div class="rte footer__text"><p>Mon – Fri, 9am – 6pm</p><p>support@petone.com</p></div></div></div>
<div class="footer__newsletter"><h3 class="footer__heading">Join the Petone pack</h3><p class="footer__text">Get exclusive deals, new launches and pet care tips.</p><form class="newsletter-form"><div class="newsletter-form__field"><input type="email" placeholder="Your email"><button class="button button--small" type="button">Subscribe</button></div></form></div></div>
<div class="footer__bottom"><form class="footer__localization"><select><option>Cambodia (USD $)</option></select></form><p class="footer__copy">© 2026 Petone. All rights reserved.</p></div></div></footer>
<script>{js}</script></body></html>'''
open(OUT,'w').write(html)
print('written', len(html))
