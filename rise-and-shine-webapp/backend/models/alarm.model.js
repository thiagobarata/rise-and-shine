import mongoose from 'mongoose';

const alarmSchema = new mongoose.Schema({
    username: { type: String, required: true },
    alarm_time: { type: String, required: true },
    timestamp: { type: String, required: true },
    soundfile: { type: String, default: "alarm1.mp3" },
    enabled: { type: Boolean, default: true }
  }, { collection: 'alarm' });  // <- force exact collection name
  
  const Alarm = mongoose.model('Alarm', alarmSchema);
  export default Alarm;
  