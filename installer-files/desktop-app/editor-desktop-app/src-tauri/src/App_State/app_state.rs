use std::sync::{Arc, Mutex};
use std::sync::mpsc::Sender;
use serde_json::Value;

// This struct keeps track of any necessary state variables for the entire application
// All variables must be thread safe so that different Rust threads can access the
// variables without corruption from other threads
pub struct AppState {
    //simple bool for whether the home page is fully mounted
    // This changes via the Is_GUI_Loaded command
    pub gui_loaded: Arc<Mutex<bool>>,

    // The app needs a way to communicate with the background thread responsible for script communication
    pub event_sender: Mutex<Sender<Value>>,

    // Add more state variables as needed

}

