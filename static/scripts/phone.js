function validatePhoneKey(e) {
  const key = e.key;
  const allowedKeys = ['+', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6',
                      'Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'];

  // Разрешаем: цифры, +, управляющие клавиши
  if (!allowedKeys.includes(key)) {
    e.preventDefault();
    return false;
  }

  // Запрещаем + не в начале
  const input = e.target;
  if (key === '+' && input.selectionStart !== 0) {
    e.preventDefault();
    return false;
  }

  return true;
}

// Автоматическая коррекция ввода
function processPhoneInput(input) {
  let value = input.value;

  // Удаляем все нецифры и лишние плюсы
  value = value.replace(/[^\d+]/g, '');

  // Оставляем только первый плюс
  const hasPlus = value.indexOf('+') > -1;
  value = value.replace(/\+/g, '');
  if (hasPlus) value = '+' + value;

  // Ограничение длины
  const maxLength = input.getAttribute('maxlength');
  if (value.length > maxLength) {
    value = value.slice(0, maxLength);
  }

  // Автозамена 8 на +7
  if (value.startsWith('8') && value.length === 1) {
    value = '+7';
  }

  input.value = value;
}