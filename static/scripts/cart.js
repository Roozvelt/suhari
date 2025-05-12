document.addEventListener('DOMContentLoaded', function() {

    console.log('Script loaded!'); // Проверка загрузки

    // Обработчики для кнопок +/-
    document.querySelectorAll('.plus-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            input.value = parseInt(input.value) + 1;
        });
    });

    document.querySelectorAll('.minus-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            if (parseInt(input.value) >= 1) {
                input.value = parseInt(input.value) - 1;
            }
        });
    });
});