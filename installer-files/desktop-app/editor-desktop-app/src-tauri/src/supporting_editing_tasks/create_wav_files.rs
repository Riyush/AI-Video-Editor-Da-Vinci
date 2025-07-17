use std::collections::HashMap;
use std::process::{Command, Stdio};
use std::io::{self, Write};
use std::fs;
use std::env;
use std::path::{Path, PathBuf};

pub fn create_wav_files_using_python(paths_dict: HashMap<usize, Vec<String>>) -> Result<String, Box<dyn std::error::Error>> {
    // Get path to current executable
    let exe_path = env::current_exe()?;
    let project_root = exe_path
        .parent().unwrap() // /target/debug/
        .parent().unwrap() // /target/
        .parent().unwrap(); // src-tauri

    // Path to the Python file relative to project root
    let py_path = project_root.join("python").join("convert_media_to_wav.py");
    println!("python file path: {}", py_path.display());

    if !py_path.exists() {
        return Err(format!("Python script not found at: {}", py_path.display()).into());
    }

    let paths_str: &str = &serde_json::to_string(&paths_dict).unwrap();
    println!("Paths as str: {}", paths_str);

    // spawn a child process to execute the python function to get .wav files
    let mut child = Command::new("python3")
    .arg(py_path)
    .stdin(Stdio::piped())
    .stdout(Stdio::piped())
    .spawn()?;

    // give the child process the paths dictionary to parse
    child.stdin.as_mut().unwrap().write_all(paths_str.as_bytes())?;

    let output = child.wait_with_output()?;

    if output.status.success() {
        
        let stdout_str = String::from_utf8(output.stdout)?;
        println!("Python script output:\n{}", stdout_str);  // 👈 see all prints + result
        // This works, the dictionary of track to wav files is returned as a string
        // in the standard output string. We can, now return this and create a 
        // function to create the silence timestamps
        Ok(stdout_str)
    } else {
        Err(format!(
            "Python error: {}",
            String::from_utf8_lossy(&output.stderr)
        )
        .into())
    }
}

