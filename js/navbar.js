function loadNavbar(activePage) {
    const path = window.location.pathname;

    const inPages = path.includes("/pages/");
    const inTexts = path.includes("/texts/");

    const homeHref = inPages || inTexts ? "../index.html" : "index.html";

    let pagesPrefix;
    if (inPages) {
        pagesPrefix = "";
    } else if (inTexts) {
        pagesPrefix = "../pages/";
    } else {
        pagesPrefix = "pages/";
    }

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
