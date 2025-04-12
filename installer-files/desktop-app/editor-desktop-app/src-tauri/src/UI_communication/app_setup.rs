use std::thread;
use std::sync::mpsc;
use tauri::{AppHandle, Manager}; // Needed for `emit_all`
use crate::script_communication::initial_connect::*;
use crate::script_communication::maintain_stream::maintain_socket_connection;

pub fn setup_app(app: &mut tauri::App) -> Result<(), Box<dyn std::error::Error>> {
    let app_handle = app.handle(); // Cloneable handle for use outside setup

    // Example global listener
    //app.listen_global("event-name", move |event| {
    //    println!("Global event received: {:?}", event.payload());
    //});

    // Check if script socket is setup and return the Unix stream
    let mut path_result = get_script_socket_path();
    let mut stream = attempt_connection(&path_result)?;

    // Create a thread to manage communication with the script
    // Simply pass the stream to a handler function 
    
    let mut app_handle_spawned_thread = app_handle.clone();
    let (event_transmitter, event_receiver ) = mpsc::channel();

    let script_comm_thread = thread::spawn(move || {
        maintain_socket_connection(stream, app_handle_spawned_thread, event_receiver)
    });
    Ok(())
}
