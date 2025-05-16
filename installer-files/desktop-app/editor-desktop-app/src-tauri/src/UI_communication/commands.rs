/*
This file is responsible for listening for events emitted by the React Frontend and
taking action on those events. These are essentially all the Tauri Commands the
Backend can receive. This ffile is linked in lib.rs

 */
use crate::App_State::app_state::AppState;
use std::io::Result;
use std::collections::HashMap;
use serde_json::Value;
use crate::utils::type_check::print_type_of;

// This is a command that gets called when the frontend has fully mounted
#[tauri::command]
pub fn GUI_Loaded(state: tauri::State<AppState>) {
    println!("GUI Loaded");
    let mut gui_loaded = state.gui_loaded.lock().unwrap();
    *gui_loaded = true;
}

// This command receives a request to do a basic edit job with user configurations
#[tauri::command]
pub fn Edit_Basic_Video(state: tauri::State<AppState>, configurations: HashMap<String, Value>) {

    println!("Received config: {:?}", configurations);
    let mut event_sender = state.event_sender.lock().unwrap();

    print_type_of(&configurations);

    // Convert HashMap<String, Value> into serde_json::Value::Object
    let config_value = Value::Object(configurations.into_iter().collect());

    if let Err(err) = event_sender.send(config_value) {
        eprintln!("Failed to send to background thread: {err}");
    }
}
