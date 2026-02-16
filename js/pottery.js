const modal = document.getElementById("potModal");
const mainImg = document.getElementById("potModalMain");
const titleEl = document.getElementById("potModalTitle");
const descEl = document.getElementById("potModalDesc");
const thumbsEl = document.getElementById("potModalThumbs");

let currentImages = [];
let currentIndex = 0;

function openModal(item) {
    const title = item.dataset.title || "";
    const desc = item.dataset.desc || "";
    const images = JSON.parse(item.dataset.images || "[]");

    currentImages = images;
    currentIndex = 0;

    titleEl.textContent = title;
    descEl.textContent = desc;

    mainImg.src = images[0] || item.querySelector("img")?.src || "";
    mainImg.alt = item.querySelector("img")?.alt || title;

    thumbsEl.innerHTML = "";
    images.forEach((src, i) => {
        const btn = document.createElement("button");
        const img = document.createElement("img");
        img.src = src;
        img.alt = `${title} thumbnail ${i + 1}`;
        if (i === 0) img.classList.add("is-active");

        btn.addEventListener("click", () => setImage(i));
        btn.appendChild(img);
        thumbsEl.appendChild(btn);
    });

    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
}

function closeModal() {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
}

function setImage(index) {
    currentIndex = index;
    mainImg.src = currentImages[index];

    [...thumbsEl.querySelectorAll("img")].forEach((img, i) => {
        img.classList.toggle("is-active", i === index);
    });
}

document.querySelectorAll(".pot-item").forEach((item) => {
    item.addEventListener("click", () => openModal(item));
    item.addEventListener("keydown", (e) => {
        if (e.key === "Enter") openModal(item);
    });
});

modal.addEventListener("click", (e) => {
    if (e.target.matches("[data-close]")) closeModal();
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("is-open")) closeModal();

    if (!modal.classList.contains("is-open")) return;

    if (e.key === "ArrowRight" && currentImages.length)
        setImage((currentIndex + 1) % currentImages.length);

    if (e.key === "ArrowLeft" && currentImages.length)
        setImage(
            (currentIndex - 1 + currentImages.length) % currentImages.length,
        );
});
