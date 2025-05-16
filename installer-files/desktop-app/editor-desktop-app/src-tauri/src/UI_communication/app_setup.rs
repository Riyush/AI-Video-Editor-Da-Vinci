use crate::script_communication::initial_connect::*;
use crate::script_communication::maintain_stream::*;
use std::sync::mpsc;
use std::thread;
use serde_json::Value;
use tauri::{AppHandle, Emitter}; // Needed for `emit_all`

pub fn setup_app(app: &mut tauri::App, event_receiver: mpsc::Receiver<Value>) -> Result<(), Box<dyn std::error::Error>> {
    let app_handle = app.handle(); // Cloneable handle for use outside setup

    // Example global listener
    //app.listen_global("event-name", move |event| {
    //    println!("Global event received: {:?}", event.payload());
    //});

    // Check if script socket is setup and return the Unix stream
    let mut path_result = get_script_socket_path();
    let mut stream = attempt_connection(path_result, app_handle.clone());

    // Create a thread to manage communication with the script
    // Simply pass the stream to a handler function

    let mut app_handle_spawned_thread = app_handle.clone();

    let script_comm_thread =
        thread::spawn(move || check_stream(stream, app_handle_spawned_thread, event_receiver));
    Ok(())
}
