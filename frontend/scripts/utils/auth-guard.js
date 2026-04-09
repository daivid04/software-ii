(function () {
  const token = localStorage.getItem('supabase_token');

  if (!token) {
    document.documentElement.style.display = 'none';
    window.location.replace("login.html");
  }
})();