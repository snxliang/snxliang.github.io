function loadNavbar(activePage) {
    // Are we currently viewing a file inside the /pages folder?
    // Works for file:// because location.pathname contains ".../pages/whatever.html"
    const inPages = window.location.pathname.includes("/pages/");

    // Link to home depends on where we are
    const homeHref = inPages ? "../index.html" : "index.html";

    // Links to other pages:
    // - from root: "pages/fiction.html"
    // - from /pages: "fiction.html" (same folder)
    const pagesPrefix = inPages ? "" : "pages/";

    const navbarHTML = `
    <nav>
        <ul class="navbar">
            <li class="navbarel"><a class="link" href="${homeHref}" data-page="home">home</a></li>
            <li class="navbarel"><a class="link" href="${pagesPrefix}fiction.html" data-page="fiction">fiction</a></li>
            <li class="navbarel"><a class="link" href="${pagesPrefix}projects.html" data-page="projects">projects</a></li>
            <li class="navbarel"><a class="link" href="${pagesPrefix}photo.html" data-page="photo">photo</a></li>
            <li class="navbarel"><a class="link" href="${pagesPrefix}about.html" data-page="about">about</a></li>
        </ul>
    </nav>
    `;

    $("#navbar").html(navbarHTML);

    if (activePage) {
        $('nav a[data-page="' + activePage + '"]').addClass("active");
    }
}
