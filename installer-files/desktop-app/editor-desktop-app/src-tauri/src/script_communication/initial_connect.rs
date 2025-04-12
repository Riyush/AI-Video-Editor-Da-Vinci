use std::os::unix::net::UnixStream;
use std::io::prelude::*;
use std::fs;
use std::path::PathBuf;
use serde::Deserialize;
use tauri::Manager;
use std::collections::HashMap;
use std::io::{self, Error, ErrorKind};

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
pub fn get_script_socket_path() -> Result<String, Box<dyn std::error::Error>> {
    let mut config_path = dirs::data_dir()  // Gets ~/Library/Application Support on macOS
        .ok_or("Could not find user data directory")?;

    config_path.push("AI-Video-Editor/ipc_config.json");

    // Try to read and parse config, unify all failure cases
    let config_content = fs::read_to_string(&config_path)
        .map_err(|_| "Script not yet run: ipc_config.json not available")?;

    let ipc_config: IPCConfig = serde_json::from_str(&config_content)
        .map_err(|_| "Script not yet run: ipc_config.json is malformed")?;

    Ok(ipc_config.socket_path)
}
// Attempt to connect to the socket path. The success vs failure of this function needs to 
// trigger a different page in the frontend. Also, return the connection for future use in the program
pub fn attempt_connection(socket_path: &Result<String, Box<dyn std::error::Error>>) -> std::io::Result<(UnixStream)> {

    match socket_path{
        Ok(socket_path) => {
            // Connect to socket
            let mut stream = UnixStream::connect(socket_path)?;

            // Use match to create global tauri event 
            let mut parameters = HashMap::new();
            send_message_via_socket(&mut stream, String::from("GUI_Startup"), parameters);

            return Ok(stream) // Preserve the stream to handle incoming messages from the script
        }
        Err(e) if e.to_string().contains("Script not yet run") => {
            todo!();
            // Create Tauri event that shows the page prompting user to run script 

            Err(Error::new(ErrorKind::NotFound, "Script not yet run"))
        }
        Err(e) => {
            // Log or show unexpected error
            eprintln!("Unexpected IPC error: {}", e);
            Err(Error::new(ErrorKind::Other, format!("Unexpected IPC error: {}", e)))
        }
    }


}