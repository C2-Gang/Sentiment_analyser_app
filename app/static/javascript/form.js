  $(document).ready(function(){
    var button = document.getElementById("button")
    $(button).on('click',function(event){
      $("#output_sentiment").html("");
      var text = document.getElementById("piecetext").value
      $.ajax({
        url: "/handle",
        type: "get",
        data: {jsdata: text},
        success: function(response) {
          $("#output_sentiment").append(response)
        },
        error: function(xhr) {
          //Do Something to handle error
        }
      });

      });
  });
