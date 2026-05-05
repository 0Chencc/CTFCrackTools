mod commands;
mod crypto;
mod encoding;
mod hash;
mod text;

use commands::{base64_decode, base64_encode, execute_workflow};

/// Portable 模式：若 exe 同目录存在 WebView2/ 子目录，指向它而非系统 WebView2。
/// 不存在时静默回退，对 NSIS 安装版 / 裸 exe 均无副作用。
#[cfg(target_os = "windows")]
fn setup_portable_webview2() {
    let Some(wv2) = std::env::current_exe()
        .ok()
        .and_then(|exe| exe.parent().map(|dir| dir.join("WebView2")))
    else {
        return;
    };
    if wv2.is_dir() {
        std::env::set_var("WEBVIEW2_BROWSER_EXECUTABLE_FOLDER", &wv2);
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    #[cfg(target_os = "windows")]
    setup_portable_webview2();

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
