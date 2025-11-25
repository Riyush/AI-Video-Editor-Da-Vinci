use std::collections::HashMap;
use std::process::{Command, Stdio};
use std::io::{self, Write};
use std::path::{Path, PathBuf};
use std::error::Error;
use serde_json::Value;
use serde_json;
use std::os::unix::net::UnixStream;

use crate::script_communication::send_socket_message::send_message_via_socket;

pub fn create_wav_files_using_python(paths_dict: HashMap<usize, Vec<String>>, stream: &mut UnixStream) -> Result<String, Box<dyn Error>> {
    // Get path to the production python interpreter
    let python_interpreter_MAC = String::from("/Library/Application Support/GameTime/main_logic/production_env/bin/python3.12");
    
    // Get path to create_wav_files script in production environment
    let py_path_MAC = PathBuf::from("/Library/Application Support/GameTime/main_logic/Basic_Edit_Job/supporting_edit_tasks/convert_media_to_wav.py");

    println!("python file path: {}", py_path_MAC.display());

    if !py_path_MAC.exists() {
        return Err(format!("Python script not found at: {}", py_path_MAC.display()).into());
    }

    let paths_str: &str = &serde_json::to_string(&paths_dict).unwrap();
    println!("Paths as str: {}", paths_str);

    // spawn a child process to execute the python function to get .wav files
    // use the python interpreter installed on the user's system.
    let mut child = Command::new(python_interpreter_MAC)
    .arg(&py_path_MAC)
    .stdin(Stdio::piped())
    .stdout(Stdio::piped())
    .stderr(Stdio::piped())
    .spawn()?;

    {
    // give the child process the paths dictionary to parse
    let stdin = child.stdin.as_mut().ok_or("Failed to open stdin")?;
    stdin.write_all(paths_str.as_bytes())?;
    }
    
    let output = child.wait_with_output()?;

    if output.status.success() {
        
        let stdout_str = String::from_utf8(output.stdout)?;
        println!("Python script output:\n{}", stdout_str);  // 👈 see all prints + result
        // This works, the dictionary of track to wav files is returned as a string
        // in the standard output string. We can, now return this and create a 
        // function to create the silence timestamps
        Ok(stdout_str)
    } else {
        let stderr_str = String::from_utf8_lossy(&output.stderr).to_string();
        println!("Python script output:\n{}", stderr_str);
        let mut parameters: HashMap<String, i32> = HashMap::new();
        let serialized_payload: Value = serde_json::to_value(parameters).unwrap();
    
        send_message_via_socket(stream, stderr_str, serialized_payload);

        Err(format!("Python error: ").into())
    }
}

