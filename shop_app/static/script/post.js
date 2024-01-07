
//слухає потік подій, та повертає ref поточного вибраного міста
let city = document.getElementById("city")
city.addEventListener("change", function (){
    let currentChoice = city.value;
    console.log("Поточний вибір: " + currentChoice);

    // це запит до власного апі який поверне відділення
    const Http = new XMLHttpRequest();
    let url = "/api/"+currentChoice+"/";
    Http.open("GET", url)
    Http.send()
    Http.onreadystatechange=(e)=> {
        // це потрібно бо воно асинхронне, і починає виконуваті інші задачі до отримання всіх даних
        if (Http.readyState === 4) {if (Http.status === 200){
            let data = JSON.parse(Http.responseText)
            let warehouse = document.getElementById("warehouse") // це id cкладів
            warehouse.innerHTML = ""// це очистить список

            for (const item of data["warehouse"]){
                    let ref = item[0];
                    let wh = item[1];
                    console.log(ref);
                    console.log(wh);
                    var newOption = document.createElement("option");
                        newOption.value = ref;
                        newOption.text = wh;
                        warehouse.add(newOption)
            }
        }}}})
