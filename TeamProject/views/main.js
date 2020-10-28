// List of words to display on main page
var words = ["code", "deploy", "dev", "🐒", "create", "API", "test", "IoT", "🍌", "make", "python", "app", "🙈"]
var currWord = 0;

async function writeCode(){
  while (true){
    var word = words[currWord];
    // Write each letter with 150ms delay
    for(i = 0; i <= word.length; i++){
      await new Promise(resolve => setTimeout(resolve, 150));
      var txt = word.substring(0, i);
      document.getElementById("codeWriter").innerHTML = txt;
    }
    await new Promise(resolve => setTimeout(resolve, 1500));
    for(i = word.length; i >= 0; i--){
      await new Promise(resolve => setTimeout(resolve, 150));
      var txt = word.substring(0, i);
      document.getElementById("codeWriter").innerHTML = txt;
    }
    // increment position in list of words
    currWord++;
    // reset to start of list if done
    if(currWord >= words.length){
      currWord = 0;
    }
  }
}

$(document).ready(function() {
      $(window).scroll( function(){
        $('.gradientfadein').each( function(i){
          var bottom_of_object = $(this).offset().top + $(this).outerHeight();
          var bottom_of_window = $(window).scrollTop() + $(window).height();
          if( bottom_of_window > bottom_of_object ){
              $(this).animate({'opacity':'1'},{duration:600, queue:false});     
          }else{
              $(this).animate({'opacity':'0'},{duration:600, queue:false});   
          }
      }); 
  });
});

$(document).ready(function(){
    writeCode();
})