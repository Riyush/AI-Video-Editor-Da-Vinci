// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

// Bring in the AppState struct which safely holds global state variables
// Note, this needs to be managed by the Tauri builder
use GameTime_lib::App_State::app_state::AppState; 

// Get the Tauri Commands:
use GameTime_lib::UI_communication::commands;
// Get the Setup app function
use GameTime_lib::UI_communication::app_setup::setup_app;
use tauri_plugin_opener;

// Define backend behaviors of the script
fn main() {
    println!("HELLO from rust app");

    let mut state = AppState::default();  // create a struct managing all state variables

    tauri::Builder::default()
        .manage(state)
        .invoke_handler(tauri::generate_handler![
            commands::GUI_Loaded,
        ])
        .plugin(tauri_plugin_opener::init())
        .setup(|app| setup_app(app)) // setup app configures state information before launching the actual application
        .run(tauri::generate_context!())
        .expect("failed to run app");
}
