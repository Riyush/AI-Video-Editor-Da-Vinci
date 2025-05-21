use serde_json::Value;
use std::collections::HashMap;
use std::option;
use std::os::unix::net::UnixStream;
use tauri::{AppHandle, Emitter}; // Needed for `emit_all`

use crate::UI_communication::event_creation_handler::send_global_message;

/* This function acts as a handler receiving socket messages and calling
send_socket_message as needed to communicate with the script */
pub fn socket_response_handler(response: String, app: AppHandle) {
    // Consider that in the future, all responses will be in JSON format
    let parsed: Result<HashMap<String, Value>, _> = serde_json::from_str(&response);

    //match &parsed {
    //Ok(map) => println!("{:#?}", map), // Pretty-print the map
    //Err(e) => eprintln!("Failed to parse JSON: {}", e),
    //}

    match parsed {
        Ok(map) => {
            match map.get("type").and_then(|v| v.as_str()) {
                Some("GUI_Startup_Success") => {
                    // Script is run
                    let parameters: HashMap<String, String> = HashMap::new();
                    // Emit event prompting login page to frontend
                    send_global_message(app, "socket_success", parameters);
                }
                // add response handling for other values of type key
                Some(other_type) => {
                    // Parse unexpectev values of type
                    println!("Received unexpected type: {}", other_type);
                }
                None => {
                    // Pase when there is no type field
                    println!("No 'type' field in response.");
                }
            }
        }
        Err(e) => {
            println!("Failed to parse response as JSON: {}", e);
        }
    }
}
