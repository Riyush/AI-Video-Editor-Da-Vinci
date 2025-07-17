use serde::Deserialize;
use serde_json;
use std::collections::HashMap;
use std::fs;
use std::io::prelude::*;
use std::io::{self, Error, ErrorKind};
use std::option;
use std::os::unix::net::UnixStream;
use std::path::PathBuf;

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
    // First, check try global Application Support
    let mut global_config_path =
        PathBuf::from("/Library/Application Support/AI-Video-Editor/ipc_config.json");

    if global_config_path.exists() {
        return Some(global_config_path.to_string_lossy().into_owned());
    }

    // Then try /tmp directory
    let mut tmp_config_path = PathBuf::from("/tmp/ipc_config.json");

    if tmp_config_path.exists() {
        return Some(tmp_config_path.to_string_lossy().into_owned());
    }

    None
}
// Attempt to connect to the socket path. The success vs failure of this function needs to
// trigger a different page in the frontend. Also, return the connection for future use in the program
pub fn attempt_connection(config_path: Option<String>, app: AppHandle) -> Option<UnixStream> {
    match config_path {
        Some(path) => {
            let config_content = fs::read_to_string(&path)
                .map_err(|e| {
                    std::io::Error::new(
                        std::io::ErrorKind::Other,
                        format!("Failed to read file: {}", e),
                    )
                })
                .ok()?;

            let ipc_config: IPCConfig = serde_json::from_str(&config_content)
                .map_err(|e| {
                    std::io::Error::new(
                        std::io::ErrorKind::InvalidData,
                        format!("Malformed config: {}", e),
                    )
                })
                .ok()?;

            // Connect to socket
            let mut stream = UnixStream::connect(ipc_config.socket_path).ok()?;

            // Use match to create global tauri event
            let mut parameters: serde_json::Value = serde_json::to_value(HashMap::<String, String>::new()).unwrap();
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
