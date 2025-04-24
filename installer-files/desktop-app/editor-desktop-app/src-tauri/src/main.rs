// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use GameTime_lib::UI_communication::app_setup::setup_app;

// Define backend behaviors of the script
fn main() {
    println!("HELLO from rust app");
    tauri::Builder::default()
        .setup(|app| setup_app(app)) // setup app configures state information before launching the actual application
        .run(tauri::generate_context!())
        .expect("failed to run app");
}
