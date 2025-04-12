use tauri::{AppHandle, Emitter}; // Needed for `emit_all`
use std::collections::HashMap;
use serde::Serialize;

#[derive(Clone, Serialize)]
struct Payload {
    message: String,
}

// This function creates events based on what events are needed at the time
#[tauri::command]
fn send_global_message(app: &AppHandle, command: &str, parameters: HashMap<String, String>) {
    match command{
        "socket_success" => 
        {
            let payload = Payload {
                message: "Successfully connected to script socket".into(),
            };
            app.emit("prompt-user-to-login", payload).unwrap();
        },
        "socket_failure" =>
        {
            let payload = Payload {
                message: "Failed to connect to script socket".into(),
            };
            app.emit("prompt-user-to-run-socket-script", payload).unwrap();
        },
        _ => {
            todo!() //default case
        }
    }
}