//const app = express()
const homepage = "./public/html/home.html";
const ateampage = "./public/html/hometeam.html";
const hteampage = "./public/html/awayteam.html";
const loader = "./public/html/loader.html";
const plyloader = "./public/html/plyloader.html";
const player = "./public/html/player.html";
const start="./public/html/startteam.html"
const { spawn } = require("child_process");
const teamloader= "./public/html/teamloader.html"
var fs = require("fs");
var url = require("url");
//var fs = require('fs');
var express = require("express");
var saveme;

//http.createServer(routes.handleRequests).listen(port);

var express = require("express");
var app = express();
var server = app.listen(3000, () => console.log("App is rn"));

var bodyParser = require("body-parser");
app.use(bodyParser.json({ limit: "50mb" }));
app.use(bodyParser.urlencoded({ limit: "50mb", extended: true }));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(__dirname + "/public"));
app.get("/", (req, res) => {
  res.writeHead(200, { "Content-Type": "text/html" });
  renderHTML(homepage, res);

});

app.get("/team1", (req, res) => {
  res.writeHead(200, { "Content-Type": "text/html" });
  renderHTML(ateampage, res);
});
app.get("/team2", (req, res) => {
  res.writeHead(200, { "Content-Type": "text/html" });
  renderHTML(hteampage, res);
});
app.get("/loading", (req, res) => {
  res.writeHead(200, { "Content-Type": "text/html" });
  renderHTML(loader, res);
});
app.get("/plyloading", (req, res) => {
  res.writeHead(200, { "Content-Type": "text/html" });
  renderHTML(plyloader, res);
});
app.get("/player", (req, res) => {
  res.writeHead(200, { "Content-Type": "text/html" });
  renderHTML(player, res);
});
app.get("/start", (req, res) => {
  res.writeHead(200, { "Content-Type": "text/html" });
  renderHTML(start, res);
});
app.get("/teamloader", (req, res) => {
  res.writeHead(200, { "Content-Type": "text/html" });
  renderHTML(teamloader, res);
});
const multer = require("multer");
const upload = multer();

app.post("/play", upload.none(), (req, res) => {
  //console.log(data)
  const formData = req.body;
  const data = formData.id;
  const home = formData.home;
  console.log(home);
  const away = formData.away;
  console.log(away);

  let match = {
    id: data,
  };
  let names={
    hname:home,
    aname:away, 
  }

  let data2 = JSON.stringify(match);
  let home2=JSON.stringify(names);
  fs.writeFile("./public/analysis/matchid.json", data2, (err) => {
    if (err) throw err;
    console.log("Data written to file");
  });
  fs.writeFile("./public/analysis/homename.json", home2, (err) => {
    if (err) throw err;
    console.log("Data written to file");
  });
 
  console.log(data)
  spawn("python", ["./public/script/shots.py", data]);
  spawn("python", ["./public/script/lineup.py", data]);
  spawn("python", ["./public/script/homeimg.py", home + " logo transparent"]);
  spawn("python", ["./public/script/awayimg.py", away + " logo transparent"]);
  console.log("running script!");
  // res.sendStatus(200);

  // do something with that data (write to a DB, for instance)
  res.status(200).json({
    message: "JSON Data received successfully",
  });
});

app.post("/plyloading", upload.none(), (req, res) => {
  //console.log(data)

  const formData = req.body;
  const data = formData.plyname;
  //const data=formData.plyname;
  const data2 = formData.id;
  // console.log(saveme);
  console.log(String(data) + data2);
  spawn("python", ["./public/script/player_analysis.py", data2, data]);
  spawn("python", ["./public/script/img.py", data + " soccer headshot"]);

  //console.log("running script!")
  // res.sendStatus(200);

  // do something with that data (write to a DB, for instance)
});

function renderHTML(path, response) {
  fs.readFile(path, null, function (error, data) {
    if (error) {
      //Something went wrong, we couldn't find the page, just 404
      response.writeHead(404);
      response.write("File not found!");
    } else {
      //We found the requested file, write it to the response.
      console.log(path + " requested.");
      response.write(data);
    }
    response.end(); //End the response.
  });
}
