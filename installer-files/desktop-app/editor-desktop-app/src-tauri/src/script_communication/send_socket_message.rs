use serde_json::Value;
use std::collections::HashMap;
use std::io::Write;
use std::os::unix::net::UnixStream;

// This function acts as a handler that specifies custom messages sent via the unix socket
// All messages take on the same json format, but may require different preprocessing steps
pub fn send_message_via_socket(
    stream: &mut UnixStream,
    message_type: String,
    parameters: HashMap<String, String>,
) -> std::io::Result<()> {
    let payload: Value = match message_type.as_str() {
        "GUI_Startup" => {
            // You can manipulate or preprocess parameters here if needed
            serde_json::json!({
                "type": message_type,
                "params": parameters
            })
        }
        "Basic-Edit-Job" => {
            serde_json::json!({
                "type": message_type,
                "params": parameters
            })
        }
        _ => {
            // Default handler for other message types
            serde_json::json!({
                "type": message_type,
                "params": parameters
            })
        }
    };
    let serialized = payload.to_string();


    stream.write_all(serialized.as_bytes())?;
    stream.flush()?;

    Ok(())
}
