function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function submitForm() {

    // особисті дані
    let name = document.getElementById("full_name").value
    let surname = document.getElementById("surname").value
    let patronymic = document.getElementById("patronymic").value
    let cart_id = document.getElementById("cart_id").value
    let phone = document.getElementById("phone").value

    // місто доставки
    let city = document.getElementById("city")
    let selectedcity = city.options[city.selectedIndex].text;

    // відділення НП
    let warehouse = document.getElementById("warehouse");
    let index = warehouse.selectedIndex;
    let selectedWarehouse = null;
    if (index>=0){selectedWarehouse = warehouse.options[index].text;}

    // назви товарів
    let productNames = document.getElementsByName("product-name").values()
    let prodNamesArray = [];
    for (let element of productNames) {
        prodNamesArray.push(element.textContent)};

    //  кількості товарів
    let productAmounts = document.getElementsByName("product-amount")
    let prodAmountsArray = [];
    for (let element of productAmounts) {
        prodAmountsArray.push(element.textContent)};

    // вартості за одиницю товару
    let productPrices = document.getElementsByName("product-price")
    let prodPricesArray = [];
    for (let element of productPrices) {
        prodPricesArray.push(element.textContent)};

    // токен
    let csrftoken = getCookie('csrftoken');

    // перевіряємо чи заповнено всі поля
    if (selectedWarehouse && name && surname && patronymic && phone && prodNamesArray.length>0) {
        console.log(prodNamesArray)
        // формуємо дані для відправки
        let requestData = {
            "cart_id": cart_id,
            "name": name,
            "surname": surname,
            "patronymic": patronymic,
            "phone": phone,
            "selectedcity": selectedcity,
            "selectedWarehouse": selectedWarehouse,
            "prodNamesArray": prodNamesArray,
            "prodAmountsArray": prodAmountsArray,
            "prodPricesArray": prodPricesArray
        };
        let jsonData = JSON.stringify(requestData);

        // це запит до власного апі яке надішле повідомлення в телегу і зробить ще купу іншого бруду)
        const Http = new XMLHttpRequest();
        let url = "/order/";
        Http.open("POST", url)
        Http.setRequestHeader("X-CSRFToken", csrftoken);
        Http.send(jsonData)
        Http.onreadystatechange=(e)=> {

            if (Http.readyState === 4) {if (Http.status === 200){
                let data = JSON.parse(Http.responseText)
                console.log(data)
            }}}


        alert("Замовлення прийнято")
        // це редірект на головну сторінку
        document.location.href = '/main/all/1'}
        else {
            if (prodNamesArray.length<=0){
                alert("Корзина пуста")
            }
            else {alert("Заповніть всі поля")}
        }
    }

