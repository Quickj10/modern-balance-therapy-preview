(function(){
  var yr=document.getElementById('yr'); if(yr) yr.textContent=new Date().getFullYear();
  var hdr=document.querySelector('header.site'), btn=document.querySelector('.menu-btn'), panel=document.getElementById('mnav');
  if(!hdr||!btn||!panel) return;
  function setOpen(on){
    hdr.classList.toggle('open',on); panel.hidden=!on; document.documentElement.classList.toggle('menu-open',on);
    btn.setAttribute('aria-expanded',on?'true':'false'); btn.setAttribute('aria-label',on?'Close menu':'Open menu');
    document.body.style.overflow=on?'hidden':'';
  }
  btn.addEventListener('click',function(){ setOpen(panel.hidden); });
  panel.addEventListener('click',function(e){ if(e.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape' && !panel.hidden){ setOpen(false); btn.focus(); } });
  document.addEventListener('click',function(e){ if(!panel.hidden && !hdr.contains(e.target)) setOpen(false); });
  window.addEventListener('resize',function(){ if(window.innerWidth>900 && !panel.hidden) setOpen(false); });
})();
