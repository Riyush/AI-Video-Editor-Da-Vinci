// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

// Bring in the AppState struct which safely holds global state variables
// Note, this needs to be managed by the Tauri builder
use GameTime_lib::App_State::app_state::AppState;

// Get the Tauri Commands:
use GameTime_lib::UI_communication::commands;
// Get the Setup app function
use tauri_plugin_opener;
use GameTime_lib::UI_communication::app_setup::setup_app;

use std::sync::mpsc;
use serde_json::Value;
use std::sync::{Arc, Mutex};

// Define backend behaviors of the script
fn main() {
    println!("HELLO from rust app");

    //create the transmitter and receiver here so I can pass transmitter to the running app
    // while I pass the receiver to the background thread that handles communication with the script
    let (event_transmitter, event_receiver) = mpsc::channel::<Value>(); 

    let mut state = AppState {
        gui_loaded: Arc::new(Mutex::new(false)),
        event_sender: Mutex::new(event_transmitter),
    }; // create a struct managing all state variables

    tauri::Builder::default()
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_opener::init())
        .manage(state)
        .invoke_handler(tauri::generate_handler![
            commands::GUI_Loaded,
            commands::Edit_Basic_Video,])
        .setup(move |app| {
            //move the receiver into setup_app
            setup_app(app, event_receiver)
        }) // setup app configures state information before launching the actual application
        .run(tauri::generate_context!())
        .expect("failed to run app");
}
