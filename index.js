import express from "express";
import bodyParser from "body-parser";
import path from "path"
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';

// Get the current directory using import.meta.url
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, 'public')));

app.use(bodyParser.urlencoded({ extended: false }));  // for form data
app.use(bodyParser.json());

app.set("view engine", "ejs");
app.set('views', path.join(path.resolve(), 'views'));


app.get("/", (req,res) => {
    res.render('index')
})
app.post("/submit", (req,res)=>{
    const formData = req.body;  // Capture form data from the request



   // Convert form data to an array (or just send the object as-is)
   const formDataArray = Object.values(formData);

   // Spawn the Python process
   const pythonProcess = spawn('python', ['./ML.py']); // Ensure ML.py is at the root level
 
   // Send data to Python script
   pythonProcess.stdin.write(JSON.stringify(formDataArray));
   pythonProcess.stdin.end();
 
   // Listen for Python script's response
   let output = '';
   pythonProcess.stdout.on('data', (data) => {
     output += data.toString();
   });
 
   pythonProcess.stderr.on('data', (data) => {
     console.error(`Python stderr: ${data.toString()}`);
   });
 
   pythonProcess.on('close', (code) => {
    if (code === 0) {
        const pythonResponse = JSON.parse(output);
  
        // Extract prediction from Python response
        const prediction = pythonResponse.prediction;
  
        // Render appropriate EJS page
        if (prediction === 0) {
          res.render('benign'); // Render benign.ejs if prediction is 0
        } else if (prediction === 1) {
          res.render('malignant'); // Render malignant.ejs if prediction is 1
        } else {
          res.status(500).send({ message: 'Unexpected prediction result', pythonResponse });
        }
      } else {
        res.status(500).send({ message: 'Error in Python script', pythonResponse: output });
      }
   });

    // res.send('ok')
})





app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
  });
  