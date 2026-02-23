/* PharmaFlow – main.js */

document.addEventListener('DOMContentLoaded', () => {

  // ── Sidebar toggle (mobile) ────────────────────────────────────
  const sidebar  = document.getElementById('sidebar');
  const overlay  = document.getElementById('sidebar-overlay');
  const hamburger = document.getElementById('hamburger');

  function openSidebar() {
    sidebar?.classList.add('open');
    overlay?.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
  function closeSidebar() {
    sidebar?.classList.remove('open');
    overlay?.classList.remove('show');
    document.body.style.overflow = '';
  }

  hamburger?.addEventListener('click', openSidebar);
  overlay?.addEventListener('click', closeSidebar);

  // ── Auto-dismiss alerts ────────────────────────────────────────
  document.querySelectorAll('.alert:not(.alert-permanent)').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    }, 4500);
  });

  // ── Delete confirmation ────────────────────────────────────────
  // Handled via Bootstrap modal – see confirm_delete.html

  // ── Active nav link ────────────────────────────────────────────
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item[href]').forEach(el => {
    const href = el.getAttribute('href');
    if (href !== '/' && path.startsWith(href)) {
      el.classList.add('active');
    } else if (href === '/' && path === '/') {
      el.classList.add('active');
    }
  });

  // ── Purchase/Sale: auto-fill price from medicine selection ─────
  const medicineSelect = document.getElementById('id_medicine');
  const priceInput     = document.getElementById('id_total_price');
  const quantityInput  = document.getElementById('id_quantity');

  if (medicineSelect && priceInput && quantityInput) {
    // Price data embedded in option data attributes (set in template)
    function updatePrice() {
      const opt = medicineSelect.options[medicineSelect.selectedIndex];
      const unitPrice = parseFloat(opt?.dataset?.price || 0);
      const qty = parseInt(quantityInput.value || 1);
      if (unitPrice && qty) {
        priceInput.value = (unitPrice * qty).toFixed(2);
      }
    }
    medicineSelect.addEventListener('change', updatePrice);
    quantityInput.addEventListener('input', updatePrice);
  }
});
