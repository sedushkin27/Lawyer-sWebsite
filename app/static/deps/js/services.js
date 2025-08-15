document.addEventListener('DOMContentLoaded', () => {
    initOpeningList();
});

function initOpeningList() {
    const openingList = document.getElementById('opening-list-services');
    const listServices = document.querySelector('.list-services');

    if (openingList && listServices) {
        openingList.addEventListener('click', (event) => {
            event.stopPropagation();
            openingList.classList.toggle('active');
            listServices.classList.toggle('active');
        });

        document.addEventListener('click', (event) => {
            if (!openingList.contains(event.target) && !listServices.contains(event.target)) {
                openingList.classList.remove('active');
                listServices.classList.remove('active');
            }
        });
    }
}