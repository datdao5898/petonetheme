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
      this.onScroll = () => {
        this.classList.toggle('is-scrolled', window.scrollY > 10);
        const rect = this.getBoundingClientRect();
        document.documentElement.style.setProperty('--header-bottom', Math.max(rect.bottom, 0) + 'px');
      };
      window.addEventListener('scroll', this.onScroll, { passive: true });
      window.addEventListener('resize', this.onScroll);
      this.onScroll();

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
      window.removeEventListener('resize', this.onScroll);
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
  const revealTargets = '.section-head, .bundle-card, .carousel__slide, .story-panel, .stat, .faq-item, .trust-item, .product-grid > li, .article-card, .collection-tile';
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
