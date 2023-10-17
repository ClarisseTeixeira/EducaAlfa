document.addEventListener('DOMContentLoaded', function () {
    const accordionItems = document.querySelectorAll('.accordion-item');

    accordionItems.forEach(function (item) {
        const button = item.querySelector('.accordion-button');
        const collapse = item.querySelector('.accordion-collapse');

        collapse.addEventListener('show.bs.collapse', function () {
            item.classList.add('open');
        });

        collapse.addEventListener('hide.bs.collapse', function () {
            item.classList.remove('open');
        });
    });
});
