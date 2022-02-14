
//const app = express()
const homepage = './public/html/home.html';
const teampage = './public/html/welcome.html';
const loader = './public/html/loader.html';
const {spawn} = require('child_process'); 
var fs = require('fs');
var url = require('url');
//var fs = require('fs');
var express = require('express');

//http.createServer(routes.handleRequests).listen(port);

var express = require('express'); 
var app = express(); 
var server = app.listen(3000, ()=>console.log("App is rn")); 
  
var bodyParser = require('body-parser');
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));
app.use(bodyParser.urlencoded({ extended: true })); 
app.use(express.static(__dirname + '/public'));
app.get('/', (req, res) => { 
    res.writeHead(200, {'Content-Type': 'text/html'});
                     renderHTML(homepage, res);
    
                    });


                    app.get('/team', (req, res) => { 
                        res.writeHead(200, {'Content-Type': 'text/html'});
                                         renderHTML(teampage, res);
                        
                                        });
                                        app.get('/loading', (req, res) => { 
                                            res.writeHead(200, {'Content-Type': 'text/html'});
                                                             renderHTML(loader, res);
                                            
                                                            });                                 
 const multer = require('multer');
const upload = multer();

app.post('/play', upload.none(), (req, res) => { 

		//console.log(data)
        const formData = req.body;
        const data=formData.id;
        console.log(data)
        spawn('python', ['./public/script/shots.py', data]);
        spawn('python', ['./public/script/lineup.py', data]);
        console.log("running script!")
       // res.sendStatus(200);
	
    // do something with that data (write to a DB, for instance) 
	res.status(200).json({ 
		message: "JSON Data received successfully" 
	}); 
});


function renderHTML(path, response){
    fs.readFile(path, null, function(error, data) {
        if (error) { //Something went wrong, we couldn't find the page, just 404
            response.writeHead(404);
            response.write('File not found!');
        }
        else { //We found the requested file, write it to the response.
            console.log(path + ' requested.');
            response.write(data);
        }
        response.end(); //End the response.
    });
}