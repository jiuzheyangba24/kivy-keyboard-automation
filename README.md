# 🎯 ikun牌高效键盘自动化工具

这是一个基于Kivy开发的移动端键盘自动化应用。

## ✨ 功能特点

- 🚀 高效的键盘输入自动化
- 📱 移动端友好的触摸界面
- ⚙️ 可自定义的输入参数
- 🔄 支持重复输入功能

## 🏗️ 自动构建

本项目使用GitHub Actions自动构建Android APK文件。
每次推送代码都会自动触发构建流程。

### 📱 下载APK

1. 进入 [Actions](../../actions) 页面
2. 选择最新的成功构建
3. 下载 `android-apk` 文件
4. 解压获取APK文件

## 🛠️ 本地开发

```bash
# 安装依赖
pip install kivy buildozer

# 运行应用
python main.py

# 构建APK（需要Linux环境）
buildozer android debug
```

## 📄 许可证

MIT License