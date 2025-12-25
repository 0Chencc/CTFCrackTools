mod commands;
mod crypto;
mod encoding;
mod hash;
mod text;

use commands::{base64_decode, base64_encode, execute_workflow};

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_log::Builder::default().build())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .invoke_handler(tauri::generate_handler![
            base64_encode,
            base64_decode,
            execute_workflow,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
