// отримуємо інпут у змінну
let search = document.getElementById("searchbar");
// отримуємо список у змінну
let list= document.getElementById("search-menu");

let body = document.getElementById("body")

// прослуховувач потоку
search.addEventListener("input", function () {

    // критерій пошуку
    let criterial = search.value

    // це очищує результати пошуку
    if (search.value === "") {list.innerHTML = "";}



    // це запит до власного апі який поверне відділення
    const Http = new XMLHttpRequest();
    let url = "/search/"+criterial+"/";
    Http.open("GET", url)
    Http.send()
    Http.onreadystatechange=(e)=> {
        // це потрібно бо воно асинхронне, і починає виконуваті інші задачі до отримання всіх даних
        if (Http.readyState === 4) {if (Http.status === 200){
            let data = JSON.parse(Http.responseText)

            // очищуємо список
            list.innerHTML = ""
            // перебираємо кожен елемент виборки
            data.forEach(function (item){console.log(item[1], item[0])

            // створення та додавання елементів списку
                let link = document.createElement("a",);
                link.className = "search-res-item"
                link.href = "/product/"+item[0]+"/";
                link.innerHTML = item[1];
                list.append(link)

                search.addEventListener("mouseover", function (){
                    link.hidden=false

                })

                body.addEventListener("click", function (){
                    link.hidden = true;
                })

            })}}}});

