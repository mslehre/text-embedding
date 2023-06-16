
//function to get all links of a website
//function linkgrabber(){
var x = document.querySelectorAll("a");
var myarray = []
for (var i=0; i<x.length; i++){
    var nametext = x[i].textContent;
    var cleantext = nametext.replace(/\s+/g, ' ').trim();
    var cleanlink = x[i].href;
    myarray.push([cleantext,cleanlink]);
};
return myarray;
//}
