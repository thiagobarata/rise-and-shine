import mongoose from 'mongoose';

const wakeupLogSchema = new mongoose.Schema({
    username: { type: String, required: true },
    time_awake_detected: { type: String, required: true },
    duration_slept_past_alarm: { type: Number, required: true }
  }, { collection: 'wakeup_log' });
  
  const WakeupLog = mongoose.model('WakeupLog', wakeupLogSchema);
  export default WakeupLog;
  