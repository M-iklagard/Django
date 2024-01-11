let filterimg = document.getElementById("filter")
let filterrow = document.getElementById("filter-row")
let prodgrid = document.getElementById("product-grid")
filterimg.addEventListener("click", function (){

    if (filterrow.hidden){
        filterrow.hidden=false;
    prodgrid.style.marginTop="10px";
    }else {
        filterrow.hidden=true;
        prodgrid.style.marginTop="100px";
    }

})


