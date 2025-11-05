use std::sync::{Arc, Mutex};
use std::sync::mpsc::Sender;
use serde_json::{Value, json};
use serde::{Serialize, Deserialize};

// Struct that standardizes a thread message between sender and receiver
#[derive(Serialize, Deserialize, Debug)]
pub struct ThreadMessage {
    pub message_type: String,
    pub payload: Value,
}

impl ThreadMessage {
    /// Creates a new thread message with a `message_type` and any serializable payload.
    pub fn new<T: Serialize>(message_type: &str, payload: T) -> Value {
        let msg = ThreadMessage {
            message_type: message_type.to_string(),
            payload: serde_json::to_value(payload).unwrap_or(json!({})),
        };
        serde_json::to_value(msg).unwrap()  // -> Value
    }

    /// Helper if no payload is needed
    pub fn simple(message_type: &str) -> Value {
        Self::new(message_type, json!({}))
    }
}

// How to send a thread message:

//let msg = ThreadMessage::new(
//    "Basic-Edit-Job",
//    {
//        "clip_id": "abc123",
//        "volume": 0.7,
//    }
//);
//event_sender.lock().unwrap().send(msg)?;

// This struct keeps track of any necessary state variables for the entire application
// All variables must be thread safe so that different Rust threads can access the
// variables without corruption from other threads
pub struct AppState {
    //simple bool for whether the home page is fully mounted
    // This changes via the Is_GUI_Loaded command
    pub gui_loaded: Arc<Mutex<bool>>,

    // The main tauri app needs a way to communicate with the background thread responsible for script communication
    pub event_sender: Mutex<Sender<Value>>,

    // Add more state variables as needed

}