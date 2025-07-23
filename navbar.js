// navbar.js
function loadNavbar(activePage, basePath = '') {
    // If basePath is provided and doesn't end with '/', add it
    const pathPrefix = basePath ? (basePath.endsWith('/') ? basePath : basePath + '/') : '';

    const navbarHTML = `
	<nav>
	    <ul class="navbar">
		<li class="navbarel"><a class="link" href="${pathPrefix}index.html" data-page="home">home</a></li>
		<li class="navbarel"><a class="link" href="${pathPrefix}fiction.html" data-page="fiction">fiction</a></li>
		<li class="navbarel"><a class="link" href="${pathPrefix}projects.html" data-page="projects">projects</a></li>
		<li class="navbarel"><a class="link" href="${pathPrefix}photo.html" data-page="photo">photo</a></li>
		<li class="navbarel"><a class="link" href="${pathPrefix}about.html" data-page="about">about</a></li>
	    </ul>
	</nav>
    `;

    $('#navbar').html(navbarHTML);

    // Set active page
    if (activePage) {
	$('nav a[data-page="' + activePage + '"]').addClass('active');
    }
}
