  $(document).ready(function () {
  $("form").submit(function (event) {
    var formData = {
      text: $("#piecetext").val(),
    };

    $("#output_sentiment").html("");

    $.ajax({
      type: "GET",
      url: "/handle",
      data: formData,
      dataType: "json",
      encode: true,
      success: function(response) {
         $("#output_sentiment").append(response)
       },
    }).done(function (data) {
      console.log(data);
    });

    event.preventDefault();
  });
});
