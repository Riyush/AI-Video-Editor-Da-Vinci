use std::os::unix::net::UnixStream;
use std::io::prelude::*;
use std::fs;
use std::option;
use std::path::PathBuf;
use serde::Deserialize;
use std::collections::HashMap;
use std::io::{self, Error, ErrorKind};

use tauri::{AppHandle, Emitter}; // Needed for `emit_all`

use crate::script_communication::send_socket_message::send_message_via_socket;

// Define a struct that matches your JSON structure
#[derive(Deserialize, Debug)]
struct IPCConfig {
    socket_path: String,
    pid: u32,
}
// the payload type must implement `Serialize` and `Clone`.
#[derive(Clone, serde::Serialize)]
struct Payload {
  message: String,
}

// Attempt to get the path of a socket opened by the script
// NOTE: This depends on an existing file created by the script in Application Support
pub fn get_script_socket_path() -> Option<String> {
    let mut config_path = dirs::data_dir()?;  // Gets ~/Library/Application Support on macOS;

    config_path.push("AI-Video-Editor/ipc_config.json");

    // Check if the script actually created the config file
    if config_path.exists() {
        Some(config_path.to_string_lossy().into_owned())
    } else {
        None
    }

}
// Attempt to connect to the socket path. The success vs failure of this function needs to 
// trigger a different page in the frontend. Also, return the connection for future use in the program
pub fn attempt_connection(config_path: Option<String>, app: AppHandle) -> Option<UnixStream> {

    match config_path{
        Some(path) => {

            let config_content = fs::read_to_string(&path)
                .map_err(|e| std::io::Error::new(std::io::ErrorKind::Other, format!("Failed to read file: {}", e))).ok()?;

            let ipc_config: IPCConfig = serde_json::from_str(&config_content)
                .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, format!("Malformed config: {}", e))).ok()?;

            // Connect to socket
            let mut stream = UnixStream::connect(ipc_config.socket_path).ok()?;

            // Use match to create global tauri event 
            let mut parameters = HashMap::new();
            send_message_via_socket(&mut stream, String::from("GUI_Startup"), parameters);

            Some(stream) // Preserve the stream to handle incoming messages from the script
        }
        None => {
            // Create Tauri event with message:: Script not yet run
            app.emit("Script not yet run", String::from(""));
            None
        }
    }


}