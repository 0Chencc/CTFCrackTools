# Claude Code 项目规范

## 提交规范

**禁止主动提交代码。** 这是一个长期维护的大型项目，所有 commit 需要用户确认后手动执行。

- 不要自动执行 `git add` 或 `git commit`
- 不要在用户未明确要求时创建提交
- 修改代码后等待用户审查和确认

## 项目背景

CTFCrackTools 是一个 CTF (Capture The Flag) 竞赛工具箱，从 Java/Kotlin 版本迁移到 Tauri + React + TypeScript 架构。

## 技术栈

- **前端**: React 18 + TypeScript + Vite 7
- **后端**: Tauri v2 + Rust
- **状态管理**: Zustand
- **流程编辑器**: ReactFlow
- **样式**: Tailwind CSS v4 + 内联样式（主题相关）

## 开发注意事项

1. **主题切换**: 使用内联样式 + `useThemeStore` 确保同步，避免 CSS 变量延迟
2. **WebKitGTK**: 在 WSL2 环境下需要设置 `no_proxy="localhost,127.0.0.1"`
3. **表单元素**: textarea/select 需要容器背景色作为遮罩，避免主题切换闪烁
