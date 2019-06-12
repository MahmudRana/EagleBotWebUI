var outputArea = $("#chat-output");

$("#user-input-form").on("submit", function (e) {

  e.preventDefault();

  var message = $("#user-input").val();

  outputArea.append(`
    <div class='bot-message'>
      <div class='message'>
        ${message}
      </div>
    </div>
  `);

  setTimeout(function () {

    var jqXHR = $.ajax({
        type: "POST",
        url: "/login",
        async: false,
        data: { mydata: message },

    });

     result = jqXHR.responseText;
     console.log('Got back ' + result);
     var parsed_result = JSON.parse(result);
     console.log('parse:'+parsed_result.text8);
     console.log('Length ' + Object.keys(parsed_result).length);
     console.log('First ' + $(parsed_result[7]))
      for (var i in parsed_result) {
          console.log(i)
          if(i=="text8" || i=="text9" || i=="text10"){
              console.log(parsed_result[i])
            outputArea.append(`
              <div class='user-message'>
                <div class='message'>
                    <a href="${parsed_result[i]}">${parsed_result[i]}
                    </a>
                </div>
              </div>
            `);
          }else{
              console.log(parsed_result[i])
            outputArea.append(`
              <div class='user-message'>
                <div class='message'>
                    ${parsed_result[i]}
                </div>
              </div>
            `);
          }

      }
//     console.log("Link: " + parsed_result.link);

//    Print in a loop
//    for (i = 0; i < 3; i++) {
//      outputArea.append(`
//      <div class='user-message'>
//        <div class='message'>
//            ${parsed_result.link}
//        </div>
//      </div>
//    `);
//    }

//    outputArea.append(`
//      <div class='user-message'>
//        <div class='message'>
//            ${result}
//        </div>
//      </div>
//    `);

//        outputArea.append(`
//      <div class='user-message'>
//        <div class='message'>
//            ${parsed_result.text}
//        </div>
//      </div>
//    `);

  }, 250);

  $("#user-input").val("");

});
