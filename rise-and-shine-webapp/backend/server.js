/*
TRANSPARENCY about LLM use:

I used ChatGPT to help generate a lot of the boiler plate code like the model schemas and 
filling in some of these routes. It helped me do the more mindless bits of code that are more
boring to implement like all the error handling, setting up the listen, etc.




*/ 

import express from 'express';
import dotenv from 'dotenv';
import { connectDB } from './config/config_db.js';

import Alarm from './models/alarm.model.js';
import User from './models/users.model.js';
import WakeupLog from './models/wakeup_log.model.js';

import cors from 'cors';


dotenv.config({ path: '.env' });
console.log(process.env.MONGO_URI)



const app = express();
const port = 5050;


// Connect to MongoDB Atlas via Mongoose
await connectDB(); // Ensures DB connection before anything else

// Middleware to allow CORS
app.use(cors()); //allow Cross origin resource sharing
// Middleware to parse JSON
app.use(express.json());

// Health check route
app.get("/", (req, res) => {
  res.send("Server is up and running.");
});



// GET /alarm — fetch the single alarm document
app.get("/alarm", async (req, res) => {
    console.log("Entered /alarm GET Method")
  try {
    const alarm = await Alarm.findOne({});
    if (!alarm) {
      return res.status(404).json({ error: "Alarm not found" });
    }
    res.json(alarm);
  } catch (err) {
    console.error("Error fetching alarm:", err);
    res.status(500).json({ error: "Internal server error" });
  }
});

// PUT /alarm — update alarm_time, enabled, or both
app.put("/alarm", async (req, res) => {
    console.log("Entered /alarm PUT Method")
  const { alarm_time, enabled } = req.body;

  const updateFields = {};
  if (alarm_time) updateFields.alarm_time = alarm_time;
  if (enabled !== undefined) updateFields.enabled = enabled;
  updateFields.timestamp = new Date().toISOString();

  try {
    let alarm = await Alarm.findOne({});
    if (!alarm) {
      // First-time creation
      alarm = new Alarm({
        username: "thiago123",
        alarm_time: alarm_time || "",
        enabled: enabled !== undefined ? enabled : true,
        timestamp: updateFields.timestamp,
        soundfile: "alarm1.mp3"
      });
      await alarm.save();
      return res.json({ status: "Alarm created" });
    }

    // Update existing alarm
    await Alarm.updateOne({ _id: alarm._id }, { $set: updateFields });
    res.json({ status: "Alarm updated" });
  } catch (err) {
    console.error("Error updating alarm:", err);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server started on http://localhost:${port}`);
});
