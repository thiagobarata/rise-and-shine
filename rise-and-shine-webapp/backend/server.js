import express from 'express';

const app = express();

app.get("/",(req,res)=>{
    res.send("Received GET request. Server is ready");
})

app.listen(5050, () =>{
    console.log("Server started on http://localhost:5050")
})