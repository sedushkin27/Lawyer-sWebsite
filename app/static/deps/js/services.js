// const listService = document.querySelector('.services');

// if (listService) { // Проверяем, существует ли элемент
//     const serviceItems = listService.querySelectorAll('.service');

//     serviceItems.forEach((service) => {
//         const buttonService = service.querySelector('.button-service');
//         const containerService = service.querySelector('.container-service');

//         buttonService.addEventListener('click', (e) => {
//             e.preventDefault();
        
//             // Для текущего элемента
//             buttonService.classList.add('hidden');
//             buttonService.setAttribute('aria-expanded', 'false');
//             containerService.classList.remove('hidden');
//             containerService.setAttribute('aria-hidden', 'false');
        
//             // Для остальных элементов
//             serviceItems.forEach((otherService) => {
//                 if (otherService !== service) {
//                     const otherButton = otherService.querySelector('.button-service');
//                     const otherContainer = otherService.querySelector('.container-service');
        
//                     otherButton.classList.remove('hidden');
//                     otherButton.setAttribute('aria-expanded', 'true');
//                     otherContainer.classList.add('hidden');
//                     otherContainer.setAttribute('aria-hidden', 'true');
//                 }
//             });
//         });
//     });
// }