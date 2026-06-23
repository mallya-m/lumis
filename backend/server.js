const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const connectDB = require('./config/database');
connectDB();

app.use(express.json({limit:'10mb'}));
app.use(express.urlencoded({extended:true, limit:'10mb'}));

app.use(cors({
    origin : process.env.NODE_ENV === 'development' ? 'http://localhost:3000' : process.env.FRONTEND_URL ,
    methods: ['GET','POST','PUT','DELETE'],
    allowedHeaders:['Content-Type','Authorization']
}));

app.get('/',(req,res)=>{
    res.json({
        message:'LUMIS API is running',
        version:'1.0.0',
        timestamp:new Date().toISOString()
    });
});

const PORT = process.env.PORT || 5000 ;

app.listen(PORT, ()=>{
    console.log(`LUMIS backend running on http://localhost:${PORT}`);
    console.log(`Environment:${process.env.NODE_ENV}`);
});