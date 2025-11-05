use crate::App_State::app_state::AppState;
use serde::Serialize;
use std::collections::HashMap;
use std::thread;
use std::time::Duration;
use tauri::{AppHandle, Emitter, Manager}; // Needed for `emit_all`

#[derive(Clone, Serialize)]
struct Payload {
    message: String,
}

// This function emits events based on what events are needed at the time
pub fn send_global_message(app: AppHandle, command: &str, parameters: HashMap<String, String>) {
    match command {
        "socket_success" => {
            let payload = Payload {
                message: "Successfully connected to script socket".into(),
            };
            // Check for frontend to be fully mounted
            let app_clone = app.clone();

            thread::spawn(move || loop {
                let state = app_clone.state::<AppState>();
                let gui_loaded = state.gui_loaded.lock().unwrap();

                println!("[DEBUG] Checking GUI loaded state: {}", *gui_loaded);

                if *gui_loaded {
                    thread::sleep(Duration::from_millis(1000));
                    println!("[DEBUG] GUI is loaded — emitting event now.");

                    app_clone
                        .emit("prompt-user-to-login", payload.clone())
                        .unwrap();
                    break;
                }
                thread::sleep(Duration::from_millis(1000));
            });
        }
        "socket_failure" => {
            let payload = Payload {
                message: "Failed to connect to script socket".into(),
            };
            app.emit("prompt-user-to-run-socket-script", payload)
                .unwrap();
        }
        "Emit_Audio_Tracks_Count" => {
            // In this case, parameters is a hashmap <String, String> with one key value pair
            // That pair is "Audio_Track_Count" : "4"  - The javascript must convert this to int
            // Check for frontend to be fully mounted
            let app_clone = app.clone();
            // Emit event to frontend
            if let Err(err) = app_clone.emit("audio-tracks-count", parameters) {
                eprintln!("Failed to emit audio-tracks-count event: {}", err);
            }
        }
        _ => {
            todo!() //default case
        }
    }
}
