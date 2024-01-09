function submitForm() {

    // особисті дані
    let name = document.getElementById("full_name").value
    let surname = document.getElementById("surname").value
    let patronymic = document.getElementById("patronymic").value

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



    // це запит до власного апі яке надішле повідомлення в телегу
    const Http = new XMLHttpRequest();
    let url = "/order/";
    Http.open("POST", url)

    // Http.setRequestHeader("X-CSRFToken", csrfToken);
    Http.send()
    Http.onreadystatechange=(e)=> {

        if (Http.readyState === 4) {if (Http.status === 200){
            let data = JSON.parse(Http.responseText)
            console.log(data)
        }}}
    alert("Замовлення прийнято")
    // це редірект на головну сторінку
    document.location.href = '/main/all/1'
    }

