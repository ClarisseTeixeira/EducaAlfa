var navItems = document.querySelectorAll('.item-nav');

function selectLink() {
    navItems.forEach((item) => {
        item.classList.remove('ativo');
    });
    this.classList.add('ativo');
}

navItems.forEach((item) => {
    item.addEventListener('click', selectLink);
});