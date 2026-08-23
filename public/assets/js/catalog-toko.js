document.addEventListener("DOMContentLoaded", () => {

    const filters =
        document.querySelectorAll(".store-filter");

    const searchInput =
        document.querySelector("#store-search-input");

    const cards =
        document.querySelectorAll("[data-product-card]");

    let currentCategory = "all";


    function filterProducts() {

        const search =
            (searchInput?.value || "")
                .toLowerCase()
                .trim();

        cards.forEach((card) => {

            const category =
                card.dataset.category || "";

            const text =
                card.textContent
                    .toLowerCase();

            const categoryMatch =
                currentCategory === "all" ||
                category === currentCategory;

            const searchMatch =
                !search ||
                text.includes(search);

            card.hidden =
                !(categoryMatch && searchMatch);
        });
    }


    filters.forEach((button) => {

        button.addEventListener(
            "click",
            () => {

                filters.forEach((item) => {
                    item.classList.remove("active");
                });

                button.classList.add("active");

                currentCategory =
                    button.dataset.category || "all";

                filterProducts();
            }
        );

    });


    searchInput?.addEventListener(
        "input",
        filterProducts
    );

});