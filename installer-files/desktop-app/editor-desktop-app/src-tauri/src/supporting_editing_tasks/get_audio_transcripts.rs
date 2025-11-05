use std::process::{Command, Stdio};
use std::io::Write;
use std::path::PathBuf;
use std::os::unix::net::UnixStream;
use std::collections::HashMap;
use serde_json::Value;
use std::error::Error;

use crate::script_communication::send_socket_message::send_message_via_socket;

pub fn get_audio_transcripts_in_python(wav_paths_to_transcribe:Vec<String>, stream: &mut UnixStream) -> Result<String, Box<dyn Error>> {

    // Get path to the production python interpreter
    let python_interpreter = String::from("/Library/Application Support/GameTime/main_logic/production_env/bin/python3.12");
    
    // Get path to get_transcripts script in production environment
    let py_path = PathBuf::from("/Library/Application Support/GameTime/main_logic/Basic_Edit_Job/supporting_edit_tasks/get_transcriptions.py");

    println!("Python script path: {}", py_path.display());

    if !py_path.exists() {
        return Err(format!("Python script not found at: {}", py_path.display()).into());
    }

    // 3. Serialize paths list into JSON string
    // This abstracts the list of strings to a string
    let wav_paths_json = serde_json::to_string(&wav_paths_to_transcribe).unwrap();
    println!("Sending to Python: {}", wav_paths_json);

    // 4. Spawn Python process
    let mut child = Command::new(python_interpreter)
        .arg(&py_path)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    // 5. Pass JSON input to Python process via stdin
    {
        let stdin = child.stdin.as_mut().ok_or("Failed to open stdin")?;
        stdin.write_all(wav_paths_json.as_bytes())?;
    }

    let output = child.wait_with_output()?;

    if output.status.success() {
        let stdout_str = String::from_utf8(output.stdout)?;
        println!("Python transcription output:\n{}", stdout_str);

        // For now, we keep the merged transcriptions dictionary as a string
        // We will send this string back to the script for it to convert to a dictionary.
        Ok(stdout_str)
    } else {
        let stderr_str = String::from_utf8_lossy(&output.stderr).to_string();
        println!("Python transcription error:\n{}", stderr_str);

        let parameters: HashMap<String, i32> = HashMap::new();
        let serialized_payload: Value = serde_json::to_value(parameters).unwrap();
        send_message_via_socket(stream, stderr_str.clone(), serialized_payload);

        Err(format!("Python transcription error: {}", stderr_str).into())
    }
}