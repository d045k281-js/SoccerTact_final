import { createRequire } from './package-lock.json';
const require = createRequire(import.meta.url);
  const fs=require ('fs');

document.getElementById("play").addEventListener("click", teams1());
function teams1(){
        var mySelect = document.getElementById('mySelect');
        var namesteam=mySelect.options[mySelect.selectedIndex].value;
        console.log(namesteam);
     
var jsonContent = {}; // Here is your loader and modifier code
var jsonString = JSON.stringify(jsonContent, null, 4); // Pretty printed
fs.writeFileSync("./writeTo.json", jsonString);
        //console.log(namesteam.split(",")[1])
}