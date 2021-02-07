const searchBar = document.forms['searchBrand'].querySelector('input');
searchBar.addEventListener('keyup', function (e) {
    const term = e.target.value.toLocaleLowerCase();
    const brands = document.getElementsByClassName("brand");
    var notAvailable = document.getElementById('notAvailable');
    $("#titleMain").toggle($('input').val().length == 0);
    var hasResults = false;
    Array.from(brands).forEach(function (brand) {
        const title = brand.textContent;
        if (title.toLowerCase().indexOf(term) != -1) {
            console.log('salam')
            brand.parentElement.style.display = 'block';
            console.log('brand.parentElement', brand.parentElement);
            hasResults = true;
        } else {
            brand.parentElement.style.display = 'none';
        }
    });
    notAvailable.style.display = hasResults ? 'none' : 'block';
});




/* Slider */
$(function () {
    $("#price-range").slider({
        range: true, min: 0, max: 90000000, values: [1000000, 2000000], slide: function (event, ui) { $("#priceRange").val(ui.values[0] + " - " + ui.values[1]); }
    });
    $("#priceRange").val($("#price-range").slider("values", 0) + " - " + $("#price-range").slider("values", 1));

    $.ajax({

        type: "POST",
        url: "your.php",
        data: "vote=" + $("#slider-range-max").slider("value"),
        success: function (response) {
            alert(voted);

        },

    })
});

