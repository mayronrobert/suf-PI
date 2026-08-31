// Pequeninas interações: confirmação e toasts simples
document.addEventListener('click', function(e){
  const el = e.target.closest('[data-confirm]');
  if(!el) return;
  const msg = el.getAttribute('data-confirm') || 'Tem certeza?';
  if(!confirm(msg)) e.preventDefault();
});

// Função utilitária para mostrar uma notificação simples usando Bootstrap Toast se disponível
function showToast(msg){
  if(window.bootstrap && document){
    const containerId = 'app-toast-container';
    let container = document.getElementById(containerId);
    if(!container){
      container = document.createElement('div');
      container.id = containerId;
      container.style.position='fixed'; container.style.right='18px'; container.style.bottom='18px'; container.style.zIndex=9999;
      document.body.appendChild(container);
    }
    const toastEl = document.createElement('div');
    toastEl.className = 'toast align-items-center text-bg-dark border-0';
    toastEl.setAttribute('role','alert'); toastEl.setAttribute('aria-live','assertive'); toastEl.setAttribute('aria-atomic','true');
    toastEl.innerHTML = `<div class="d-flex"><div class="toast-body">${msg}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div>`;
    container.appendChild(toastEl);
    const toast = new bootstrap.Toast(toastEl,{delay:2600});
    toast.show();
    toastEl.addEventListener('hidden.bs.toast', ()=> toastEl.remove());
  } else {
    // fallback simples
    const t = document.createElement('div');
    t.textContent = msg;
    t.style.position='fixed'; t.style.right='18px'; t.style.bottom='18px';
    t.style.background='#111'; t.style.color='#fff'; t.style.padding='10px 14px';
    t.style.borderRadius='8px'; t.style.boxShadow='0 6px 18px rgba(0,0,0,0.2)';
    t.style.zIndex=9999; document.body.appendChild(t);
    setTimeout(()=> t.remove(), 2600);
  }
}

// Exemplo: escutar chamadas via HTMX para mostrar toasts quando ações POST retornarem 200
if(window.htmx){
  document.body.addEventListener('htmx:afterOnLoad', function(evt){
    const status = evt.detail.xhr && evt.detail.xhr.status;
    if(status===302 || status===200){
      const h = evt.detail.xhr.getResponseHeader && evt.detail.xhr.getResponseHeader('X-Action-Message');
      if(h) showToast(h);
    }
  });
}

// Dark-mode toggle with persistence
function setDarkMode(enabled){
  if(enabled){
    document.documentElement.classList.add('dark-mode');
    localStorage.setItem('darkMode','1');
  } else {
    document.documentElement.classList.remove('dark-mode');
    localStorage.removeItem('darkMode');
  }
}
document.addEventListener('DOMContentLoaded', function(){
  const btn = document.getElementById('theme-toggle');
  if(btn){
    const pref = localStorage.getItem('darkMode')==='1';
    setDarkMode(pref);
    btn.addEventListener('click', function(){ setDarkMode(!document.documentElement.classList.contains('dark-mode')); });
  }

  // Modal confirm handler: intercept links/buttons with data-confirm
  const confirmModalEl = document.getElementById('confirmModal');
  if(confirmModalEl && window.bootstrap){
    const confirmModal = new bootstrap.Modal(confirmModalEl);
    document.body.addEventListener('click', function(e){
      const el = e.target.closest('[data-confirm]');
      if(!el) return;
      e.preventDefault();
      const msg = el.getAttribute('data-confirm') || 'Tem certeza?';
      const ok = document.getElementById('confirmModalOk');
      document.getElementById('confirmModalMessage').textContent = msg;
      // decide action: if element is a link, copy href; if button in form, submit form on confirm
      if(el.tagName.toLowerCase()==='a' && el.href){
        ok.href = el.href;
        ok.onclick = null;
        ok.setAttribute('data-bs-dismiss','');
      } else {
        // assume button submits nearest form
        ok.href = '#';
        ok.onclick = function(ev){ ev.preventDefault(); const form = el.closest('form'); if(form) form.submit(); };
      }
      confirmModal.show();
    });
  }
});
