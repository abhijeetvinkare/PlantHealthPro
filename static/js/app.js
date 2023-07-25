window.onload = function() {
    var user = localStorage.getItem('user');
    var loginButton = document.getElementById('login-button');
    var logoutButton = document.getElementById('logout-button');
    
    if (user) {
      loginButton.style.display = 'none';
      logoutButton.style.display = 'block';
      logoutButton.style.marginTop = '13px';
    } else {
      loginButton.style.display = 'block';
      logoutButton.style.display = 'none';
    }
    
    logoutButton.addEventListener('click', function() {
      localStorage.removeItem('user');
      window.location.href = '/login';
    });
  }
  