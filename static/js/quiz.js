// function readTextFile(file)
// {
//     var rawFile = new XMLHttpRequest();
//     rawFile.open("GET", file, false);
//     rawFile.onreadystatechange = function ()
//     {
//         if(rawFile.readyState === 4)
//         {
//             if(rawFile.status === 200 || rawFile.status == 0)
//             {
//                 var allText = rawFile.responseText;
//                 alert(allText);
//             }
//         }
//     }
//     rawFile.send(null);
// }
// var d = readTextFile("/static/js/content.json");

// fetch('/static/js/content.json')
//   .then(response => response.json())
//   .then(text => console.log(text))

// console.log(text);

// answers = {};
$('#modalCFT').modal('hide');

document.getElementById("con").style.cssText = '-webkit-filter: blur(25px); -moz-filter: blur(25px); -o-filter: blur(25px); -ms-filter: blur(25px); filter: blur(25px); background: #000;';

function checkIt() {
    var a = document.getElementById('q')
    var a_value = ans.value;
    var a_name = ans.name;
    if (ans == '1') {
        document.getElementById("ctf").remove();
        document.getElementById("con").style.cssText = '-webkit-filter: blur(0px); -moz-filter: blur(0px); -o-filter: blur(0px); -ms-filter: blur(0px); filter: blur(0px); background: #fff;';
        $('#modalCFT').modal('hide');
    }
    else {

    }
}