/* Petone theme scripts */
(function () {
  'use strict';

  /* ---------- Announcement rotator ---------- */
  class AnnouncementRotator extends HTMLElement {
    connectedCallback() {
      this.items = Array.from(this.querySelectorAll('.announcement__msg'));
      if (this.items.length < 2) return;
      this.index = 0;
      const speed = (parseInt(this.dataset.speed, 10) || 5) * 1000;
      this.timer = setInterval(() => this.next(), speed);
      this.addEventListener('mouseenter', () => clearInterval(this.timer));
      this.addEventListener('mouseleave', () => { this.timer = setInterval(() => this.next(), speed); });
    }
    disconnectedCallback() { clearInterval(this.timer); }
    next() {
      this.items[this.index].classList.remove('is-active');
      this.index = (this.index + 1) % this.items.length;
      this.items[this.index].classList.add('is-active');
    }
  }
  if (!customElements.get('announcement-rotator')) customElements.define('announcement-rotator', AnnouncementRotator);

  /* ---------- Sticky header ---------- */
  class StickyHeader extends HTMLElement {
    connectedCallback() {
      const root = document.documentElement;
      const bar = this.querySelector('.header-bar') || this;
      this.onScroll = () => {
        this.classList.toggle('is-scrolled', window.scrollY > 10);
        root.style.setProperty('--header-bottom', Math.max(bar.getBoundingClientRect().bottom, 0) + 'px');
      };
      // Flow height of the header (used to pull a hero up underneath it); the framed offset doesn't change it
      this.onResize = () => {
        root.style.setProperty('--header-height', this.offsetHeight + 'px');
        this.onScroll();
      };
      window.addEventListener('scroll', this.onScroll, { passive: true });
      window.addEventListener('resize', this.onResize);
      // The framed bar animates to the top; re-measure the drawer offset once it settles
      bar.addEventListener('transitionend', this.onScroll);
      this.onResize();

      // Close other <details> panels when one opens; lock scroll for the drawer
      this.querySelectorAll('details').forEach((d) => {
        d.addEventListener('toggle', () => {
          this.onScroll();
          if (d.open) {
            this.querySelectorAll('details[open]').forEach((o) => { if (o !== d && !o.contains(d)) o.open = false; });
            if (d.classList.contains('header-search')) { const i = d.querySelector('input'); if (i) setTimeout(() => i.focus(), 50); }
          }
          document.body.style.overflow = this.querySelector('.menu-drawer[open]') ? 'hidden' : '';
        });
      });
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') this.querySelectorAll('details[open]').forEach((o) => { o.open = false; });
      });
    }
    disconnectedCallback() {
      window.removeEventListener('scroll', this.onScroll);
      window.removeEventListener('resize', this.onResize);
    }
  }
  if (!customElements.get('sticky-header')) customElements.define('sticky-header', StickyHeader);

  /* ---------- Tabs + carousel ---------- */
  class TabsComponent extends HTMLElement {
    connectedCallback() {
      this.tabs = Array.from(this.querySelectorAll('[role="tab"]'));
      this.panels = Array.from(this.querySelectorAll('[role="tabpanel"]'));
      this.prev = this.querySelector('[data-scroll="prev"]');
      this.next = this.querySelector('[data-scroll="next"]');

      this.tabs.forEach((tab, i) => tab.addEventListener('click', () => this.select(i)));
      if (this.prev) this.prev.addEventListener('click', () => this.scroll(-1));
      if (this.next) this.next.addEventListener('click', () => this.scroll(1));
      this.panels.forEach((p) => {
        const c = p.querySelector('[data-carousel]');
        if (c) c.addEventListener('scroll', () => this.updateArrows(), { passive: true });
      });
      window.addEventListener('resize', () => this.updateArrows());
      this.updateArrows();
    }
    activeCarousel() {
      const panel = this.panels.find((p) => !p.hidden) || this.panels[0];
      return panel ? panel.querySelector('[data-carousel]') : null;
    }
    select(i) {
      this.tabs.forEach((t, j) => { t.classList.toggle('is-active', i === j); t.setAttribute('aria-selected', i === j ? 'true' : 'false'); });
      this.panels.forEach((p, j) => { p.hidden = i !== j; p.classList.toggle('is-active', i === j); });
      const c = this.activeCarousel();
      if (c) c.scrollLeft = 0;
      this.updateArrows();
    }
    scroll(dir) {
      const c = this.activeCarousel();
      if (!c) return;
      const slide = c.querySelector('.carousel__slide');
      const step = slide ? slide.getBoundingClientRect().width + 20 : c.clientWidth;
      c.scrollBy({ left: dir * step, behavior: 'smooth' });
    }
    updateArrows() {
      const c = this.activeCarousel();
      if (!c || !this.prev) return;
      const max = c.scrollWidth - c.clientWidth - 2;
      this.prev.disabled = c.scrollLeft <= 2;
      this.next.disabled = c.scrollLeft >= max;
    }
  }
  if (!customElements.get('tabs-component')) customElements.define('tabs-component', TabsComponent);

  /* ---------- Hero slideshow ---------- */
  // Autoplay timing comes from the CSS progress animation on the active dot:
  // its animationend advances the slide, so pausing the animation pauses the slideshow
  // (and prefers-reduced-motion, which disables animations, disables autoplay).
  class HeroSlider extends HTMLElement {
    connectedCallback() {
      this.slides = Array.from(this.querySelectorAll('[data-slide]'));
      this.dots = Array.from(this.querySelectorAll('[data-slide-to]'));
      this.index = Math.max(0, this.slides.findIndex((s) => s.classList.contains('is-active')));
      if (this.slides.length < 2) return;

      this.querySelector('[data-slide-prev]').addEventListener('click', () => this.go(this.index - 1));
      this.querySelector('[data-slide-next]').addEventListener('click', () => this.go(this.index + 1));
      this.dots.forEach((dot, i) => {
        dot.addEventListener('click', () => this.go(i));
        dot.addEventListener('animationend', () => this.go(this.index + 1));
      });

      // Pause while the visitor is interacting or the tab is hidden
      this.holds = new Set();
      const hold = (key, on) => { on ? this.holds.add(key) : this.holds.delete(key); this.classList.toggle('is-paused', this.holds.size > 0); };
      this.addEventListener('mouseenter', () => hold('hover', true));
      this.addEventListener('mouseleave', () => hold('hover', false));
      // Only keyboard focus pauses — a mouse click on a dot shouldn't stop autoplay for good
      this.addEventListener('focusin', (e) => { if (e.target.matches(':focus-visible')) hold('focus', true); });
      this.addEventListener('focusout', (e) => { if (!this.contains(e.relatedTarget)) hold('focus', false); });
      this.onVisibility = () => hold('hidden', document.hidden);
      document.addEventListener('visibilitychange', this.onVisibility);

      this.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') this.go(this.index - 1);
        if (e.key === 'ArrowRight') this.go(this.index + 1);
      });

      // Swipe
      let startX = null;
      this.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') startX = e.clientX; });
      this.addEventListener('pointerup', (e) => {
        if (startX === null) return;
        const dx = e.clientX - startX;
        startX = null;
        if (Math.abs(dx) > 40) this.go(this.index + (dx < 0 ? 1 : -1));
      });

      // Theme editor: show the selected slide and stop rotating while editing it
      this.addEventListener('shopify:block:select', (e) => {
        const i = this.slides.indexOf(e.target);
        if (i > -1) this.go(i);
        hold('editor', true);
      });
      this.addEventListener('shopify:block:deselect', () => hold('editor', false));
    }

    disconnectedCallback() {
      if (this.onVisibility) document.removeEventListener('visibilitychange', this.onVisibility);
    }

    go(i) {
      const n = this.slides.length;
      const next = ((i % n) + n) % n;
      if (next === this.index) return;
      this.slides.forEach((slide, j) => {
        const active = j === next;
        slide.classList.toggle('is-active', active);
        slide.toggleAttribute('inert', !active);
        slide.setAttribute('aria-hidden', active ? 'false' : 'true');
        const video = slide.querySelector('video');
        if (video) active ? video.play().catch(() => {}) : video.pause();
      });
      this.dots.forEach((dot, j) => {
        dot.classList.toggle('is-active', j === next);
        j === next ? dot.setAttribute('aria-current', 'true') : dot.removeAttribute('aria-current');
      });
      this.index = next;
    }
  }
  if (!customElements.get('hero-slider')) customElements.define('hero-slider', HeroSlider);
  /* ---------- Spotlight stack ---------- */
  // Cards are position: sticky; while the next card slides over one, shrink and dim it a little.
  class StackCards extends HTMLElement {
    connectedCallback() {
      this.cards = Array.from(this.querySelectorAll('[data-stack-card]'));
      if (this.cards.length < 2 || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      this.ticking = false;
      this.onScroll = () => {
        if (this.ticking) return;
        this.ticking = true;
        requestAnimationFrame(() => { this.update(); this.ticking = false; });
      };
      window.addEventListener('scroll', this.onScroll, { passive: true });
      window.addEventListener('resize', this.onScroll);
      this.update();
    }
    disconnectedCallback() {
      if (!this.onScroll) return;
      window.removeEventListener('scroll', this.onScroll);
      window.removeEventListener('resize', this.onScroll);
    }
    update() {
      this.cards.forEach((card, i) => {
        const next = this.cards[i + 1];
        if (!next) return;
        const stickTop = parseFloat(getComputedStyle(card).top) || 0;
        const h = card.offsetHeight;
        // 0 when the next card is a full card-height below, 1 when it has fully covered this one
        const progress = Math.min(Math.max((stickTop + h - next.getBoundingClientRect().top) / h, 0), 1);
        card.style.setProperty('--stack-scale', (1 - progress * 0.06).toFixed(4));
        card.style.setProperty('--stack-dim', (progress * 0.45).toFixed(3));
      });
    }
  }
  if (!customElements.get('stack-cards')) customElements.define('stack-cards', StackCards);

  /* ---------- Shop the look ---------- */
  class LookHotspots extends HTMLElement {
    connectedCallback() {
      this.dots = Array.from(this.querySelectorAll('[data-look-dot]'));
      this.items = Array.from(this.querySelectorAll('[data-look-item]'));
      this.list = this.querySelector('.look__list');
      this.dots.forEach((dot, i) => {
        dot.addEventListener('click', () => this.select(i, true));
        dot.addEventListener('mouseenter', () => this.select(i));
        dot.addEventListener('focus', () => this.select(i));
      });
      this.items.forEach((item, i) => {
        item.addEventListener('mouseenter', () => this.select(i));
        item.addEventListener('focusin', () => this.select(i));
      });
      // Theme editor: selecting a hotspot block highlights it
      this.addEventListener('shopify:block:select', (e) => {
        const i = this.dots.indexOf(e.target);
        if (i > -1) this.select(i, true);
      });
    }
    select(i, reveal) {
      this.dots.forEach((d, j) => d.classList.toggle('is-active', i === j));
      this.items.forEach((it, j) => it.classList.toggle('is-active', i === j));
      // On mobile the list is a horizontal scroller: bring the matching product into view
      const item = this.items[i];
      if (reveal && item && this.list && this.list.scrollWidth > this.list.clientWidth) {
        this.list.scrollTo({ left: item.offsetLeft - this.list.offsetLeft, behavior: 'smooth' });
      }
    }
  }
  if (!customElements.get('look-hotspots')) customElements.define('look-hotspots', LookHotspots);

  /* ---------- Cart helpers ---------- */
  const updateCartCount = (count) => {
    document.querySelectorAll('[data-cart-count]').forEach((el) => {
      el.textContent = count;
      el.hidden = count === 0;
    });
  };

  const showToast = (item) => {
    const toast = document.getElementById('CartToast');
    if (!toast) return;
    const box = toast.querySelector('[data-toast-item]');
    box.innerHTML = '';
    if (item) {
      if (item.image) {
        const img = document.createElement('img');
        img.src = item.image + (item.image.includes('?') ? '&' : '?') + 'width=160';
        img.alt = '';
        box.appendChild(img);
      }
      const t = document.createElement('div');
      const name = document.createElement('strong');
      name.textContent = item.product_title;
      t.appendChild(name);
      if (item.variant_title) {
        const v = document.createElement('div');
        v.style.opacity = '.6';
        v.textContent = item.variant_title;
        t.appendChild(v);
      }
      box.appendChild(t);
    }
    toast.hidden = false;
    clearTimeout(toast._t);
    toast._t = setTimeout(() => { toast.hidden = true; }, 6000);
  };

  document.addEventListener('click', (e) => {
    if (e.target.closest('[data-toast-close]')) document.getElementById('CartToast').hidden = true;
  });

  /* AJAX add to cart for any form with .js-add-form */
  document.addEventListener('submit', async (e) => {
    const form = e.target.closest('form.js-add-form');
    if (!form || window.theme.cartType === 'page') return;
    e.preventDefault();
    const btn = form.querySelector('[type="submit"]');
    if (btn) { btn.disabled = true; btn.setAttribute('aria-busy', 'true'); }
    try {
      const res = await fetch(window.theme.routes.cartAdd + '.js', {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: new FormData(form)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.description || data.message || 'Error');
      const cart = await fetch(window.theme.routes.cart + '.js').then((r) => r.json());
      updateCartCount(cart.item_count);
      showToast(data.items ? data.items[0] : data);
    } catch (err) {
      const msg = form.querySelector('[data-form-error]');
      if (msg) { msg.textContent = err.message; msg.hidden = false; } else { alert(err.message); }
    } finally {
      if (btn) { btn.disabled = false; btn.removeAttribute('aria-busy'); }
    }
  });

  /* Quantity steppers */
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-qty]');
    if (!b) return;
    const input = b.parentElement.querySelector('input');
    const min = parseInt(input.min || '0', 10);
    const v = Math.max(min, (parseInt(input.value, 10) || 0) + (b.dataset.qty === 'plus' ? 1 : -1));
    input.value = v;
    input.dispatchEvent(new Event('change', { bubbles: true }));
  });

  /* Cart page: auto-submit when quantity changes */
  document.addEventListener('change', (e) => {
    if (e.target.matches('[data-cart-qty]')) {
      clearTimeout(window._cartT);
      window._cartT = setTimeout(() => e.target.form.submit(), 500);
    }
  });

  /* ---------- Reveal on scroll ---------- */
  const revealTargets = '.section-head, .bundle-card, .carousel__slide, .story-panel, .stat, .faq-item, .trust-item, .product-grid > li, .article-card, .collection-tile, .bento__grid, .look__stage, .look__panel';
  const initReveal = (root) => {
    if (!('IntersectionObserver' in window)) return;
    const els = Array.from((root || document).querySelectorAll(revealTargets)).filter((el) => !el.closest('.header-wrapper'));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach((el, i) => {
      el.classList.add('reveal');
      el.style.transitionDelay = Math.min((i % 4) * 70, 210) + 'ms';
      io.observe(el);
    });
  };
  if (!window.Shopify || !window.Shopify.designMode) initReveal();

  window.PetoneTheme = { updateCartCount, showToast };
})();
