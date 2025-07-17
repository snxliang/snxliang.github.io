// navbar.js
function loadNavbar(activePage) {
    const navbarHTML = `
	<nav>
	    <ul class="navbar">
		<li class="navbarel"><a class="link" href="index.html" data-page="home">home</a></li>
		<li class="navbarel"><a class="link" href="fiction.html" data-page="fiction">fiction</a></li>
		<li class="navbarel"><a class="link" href="projects.html" data-page="projects">projects</a></li>
		<li class="navbarel"><a class="link" href="photo.html" data-page="photo">photo</a></li>
		<li class="navbarel"><a class="link" href="about.html" data-page="about">about</a></li>
	    </ul>
	</nav>
    `;

    $('#navbar').html(navbarHTML);

    // Set active page
    if (activePage) {
	$('nav a[data-page="' + activePage + '"]').addClass('active');
    }
}
