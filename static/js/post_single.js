// var toggle = false;
// $(document).ready(function () {
//     toggle = false;
//     $(".toggle").hide();
//     $(".more-text").text("موارد بیشتر");
//     $('.red-item').hide();
//     $('.white-item').hide();

// });
// function expand() {
//     if (toggle) {
//         $(".toggle").hide();
//         toggle = false
//         $(".more-text").text("موارد بیشتر");
//     } else {
//         $(".toggle").show();
//         toggle = true
//         $(".more-text").text("بستن");
//     }
// }

// $("#black").click(function (e) {
//     e.preventDefault();
//     $("#black").css("border-color", '#5ab5cb');
//     $("#red").css('border-color', 'rgba(0,0,0,0.25)');
//     $("#white").css('border-color', 'rgba(0,0,0,0.25)');

//     $('.black-item').show();
//     $('.red-item').hide();
//     $('.white-item').hide();
// });

// $("#red").click(function (e) {
//     e.preventDefault();
//     $("#red").css("border-color", '#5ab5cb');
//     $("#black").css('border-color', 'rgba(0,0,0,0.25)');
//     $("#white").css('border-color', 'rgba(0,0,0,0.25)');


//     $('.black-item').hide();
//     $('.red-item').show();
//     $('.white-item').hide();
// });

// $("#white").click(function (e) {
//     e.preventDefault();
//     $("#white").css("border-color", '#5ab5cb');
//     $("#red").css('border-color', 'rgba(0,0,0,0.25)');
//     $("#black").css('border-color', 'rgba(0,0,0,0.25)');


//     $('.black-item').hide();
//     $('.red-item').hide();
//     $('.white-item').show();
// });


// $('#submitComment').on('click', function (e) {
//     e.preventDefault();
//     var $form = $('#commentForm');
//     var title = document.forms["commentForm"]["title"].value;
//     var body = document.forms["commentForm"]["body"].value;
//     if (title == "" || body == "") {
//         $(".message").append('<div class="alert alert-danger alert-dismissible"><a href="#" class="close" data-dismiss="alert" aria-label="close" style="text-align: right;">&times;</a>عنوان و/یا متن کامنت خالی است.</div >');
//     }
//     else {
//         $(".message").append('<div class="alert alert-success alert-dismissible">پیام با موفقیت ثبت گردید. پس از تایید در سایت نمایش داده خواهد شد.<a href="#" class="close" data-dismiss="alert" aria-label="close" style="text-align: right;">&times;</a></div >');
//         $.ajax({
//             type: "post",
//             url: "{% url 'products:laptop_view' object.slug %}",
//             data: $("#commentForm").serialize(),
//             success: function (response) {
//                 console.log(response);
//             },
//             error: function (param) {
//                 console.log(param);
//             }
//         });
//     }
// });


// function like(id, like_type) {
//     $.ajax({
//         type: "post",
//         url: "{% url 'products:like_comment' %}",
//         data: {
//             id: id,
//             like_type: like_type,
//             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
//             action: 'post',
//         },
//         success: function (json) {
//             json = JSON.parse(json)
//             like_counts = json['like_counts']
//             if (like_type == 'like') {
//                 e_id = "like_" + id;
//                 string = "Like ";
//                 document.getElementById("like_btn_" + id).className = "btn btn-success";
//             }
//             else {
//                 e_id = "dislike_" + id;
//                 string = "Dislikes ";
//                 document.getElementById("dislike_btn_" + id).className = "btn btn-danger";
//             }
//             // element = document.getElementById(e_id);
//             document.getElementById(e_id).innerHTML = string + like_counts;
//             document.getElementById("like_btn_" + id).disabled = true;
//             document.getElementById("dislike_btn_" + id).disabled = true;
//         },
//         error: function () { alert('error in liking') }
//     });
// }
