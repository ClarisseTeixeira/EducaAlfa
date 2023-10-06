document.addEventListener('DOMContentLoaded', function () {
    const accordionItems = document.querySelectorAll('.accordion-item');

    accordionItems.forEach(function (item) {
        const button = item.querySelector('.accordion-button');
        const collapse = item.querySelector('.accordion-collapse');

        // Adicione um ouvinte de evento quando um item está prestes a ser mostrado (aberto)
        collapse.addEventListener('show.bs.collapse', function () {
            item.classList.add('open');
        });

        // Adicione um ouvinte de evento quando um item está prestes a ser oculto (fechado)
        collapse.addEventListener('hide.bs.collapse', function () {
            item.classList.remove('open');
        });
    });
});
