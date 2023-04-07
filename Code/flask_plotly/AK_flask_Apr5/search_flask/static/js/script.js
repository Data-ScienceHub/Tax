$(document).ready(function () {
  $('.sidenav').sidenav();
  $('select').formSelect();
  $('.modal').modal();
});

$(".star-rating").click(function () {
  for (let i = 1; i <= 5; i++) {
    let star = "star-" + i;
    $("#"+star).removeClass("golden-star");
    $("#"+star).addClass("greyed-out");
  }
  for (let i = 1; i <= 5; i++) {
    let star = "star-" + i;
    $("#"+star).removeClass("greyed-out");
    $("#"+star).addClass("golden-star");
    if (this.id === star) {
      $("#star_score").val(i);
      break;
    }
  }

});