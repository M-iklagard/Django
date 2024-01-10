// Отримання всіх кнопок з класами decreaseBtn та increaseBtn
var decreaseBtns = document.querySelectorAll('.decreaseBtn');
var increaseBtns = document.querySelectorAll('.increaseBtn');

// Додавання обробників подій для кожної кнопки зі зменшенням кількості товару
decreaseBtns.forEach(function (btn, index) {
    btn.addEventListener('click', function () {
        decreaseAmount(index);
        updateTotalPrice();
    });
});

// Додавання обробників подій для кожної кнопки зі збільшенням кількості товару
increaseBtns.forEach(function (btn, index) {
    btn.addEventListener('click', function () {
        increaseAmount(index);
        updateTotalPrice();
    });
});

function decreaseAmount(index) {
    var amountElement = document.querySelectorAll('.amount')[index];
    var currentAmount = parseInt(amountElement.textContent);
    if (currentAmount > 1) {
        amountElement.textContent = currentAmount - 1 + ' шт';
    }
}

function increaseAmount(index) {
    var amountElement = document.querySelectorAll('.amount')[index];
    var currentAmount = parseInt(amountElement.textContent);
    amountElement.textContent = currentAmount + 1 + ' шт';
}

function updateTotalPrice() {
    var productBlocks = document.querySelectorAll('.product-block');
    var totalPrice = 0;

    productBlocks.forEach(function (productBlock, index) {
        var quantity = parseInt(productBlock.querySelector('.amount').textContent);
        var price = parseFloat(productBlock.querySelector('.price').textContent);

        totalPrice += quantity * price;
    });

    // Оновлення загальної вартості
    var totalPriceElement = document.getElementById('totalPrice');
    totalPriceElement.textContent = 'Загальна вартість: ' + totalPrice.toFixed(2) + ' грн';
}
