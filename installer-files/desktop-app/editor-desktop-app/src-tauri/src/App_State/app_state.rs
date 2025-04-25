use std::sync::{Arc, Mutex};

// This struct keeps track of any necessary state variables for the entire application
// All variables must be thread safe so that different Rust threads can access the
// variables without corruption from other threads
#[derive(Clone, Default)]
pub struct AppState {
    //simple bool for whether the home page is fully mounted
    // This changes via the Is_GUI_Loaded command
    pub gui_loaded: Arc<Mutex<bool>>,
    // Add more state variables as needed
}