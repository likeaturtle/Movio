# Movio 项目对比分析：相比原版 DeskHop 的优化与更新

**上游项目**: [hrvach/deskhop](https://github.com/hrvach/deskhop)  
**本项目**: [likeaturtle/Movio](https://github.com/likeaturtle/Movio)  
**基准点**: commit `be55d7f` (Bugfixes)  
**统计**: 39 个文件变更，+1042 行 / -273 行

---

## 一、品牌重塑 (Brand Identity)

将原版 "DeskHop" 全面更名为 "Movio"，涉及以下层面：

| 层面 | 原版 (DeskHop) | 本项目 (Movio) |
|------|---------------|----------------|
| USB 厂商名称 | `Hrvoje Cavrak` | `Movio` |
| USB 产品名称 | `DeskHop Switch` | `Movio Switch` |
| 辅助接口名 | `DeskHop Helper / Config / Disk / Debug` | `Movio Helper / Config / Disk / Debug` |
| RAM 磁盘卷标 | `DESKHOP` | `MOVIO` |
| CMake 项目名 | `deskhop_project` | `movio_project` |
| 二进制产物名 | `deskhop.uf2` | `movio.uf2` |
| CI 产物名 | `deskhop-gha-{n}` | `movio-gha-{n}` |
| Docker 镜像/路径 | `deskhop-build` / `/deskhop` | `movio-build` / `/movio` |
| udev 规则文件名 | `99-deskhop.rules` | `99-movio.rules` |
| 配置页面标题 | `DeskHop Config` | `Movio Function Config` |
| 主色调 | `#5e9f41` (绿色) | `#ff6600` (橙色) |

---

## 二、Web 配置界面优化

### 2.1 中英文国际化 (i18n)

为配置页面添加了完整的中英文双语支持：

- **实现方式**: 纯前端 JS 模块 (`i18n`)，基于 `data-i18n` 属性标记可翻译元素
- **语言切换**: 页面右上角 `EN / 中文` 切换按钮
- **记忆功能**: 使用 `localStorage` 存储用户语言偏好 (`movio-lang`)
- **覆盖范围**: 所有 UI 文本，包括：
  - 导航按钮（连接/读取/保存/退出等）
  - 配置标签（屏幕数量/速度/边界等）
  - 下拉选项值（操作系统/屏幕位置等）
  - 状态信息和错误提示
- **默认语言**: 中文

### 2.2 视觉设计改进

- **主题色**: 从绿色 (`#5e9f41`) 改为橙色 (`#ff6600`)
- **图标重新设计**:
  - 左侧导航栏：使用自定义 SVG 鼠标+键盘组合图标（替代原版键盘 SVG）
  - Output A/B：使用显示器外形 SVG，内嵌 "Movio A"/"Movio B" 文字标识
  - 添加页面 favicon（SVG base64 内嵌）
- **保存按钮**: 移至页面右下角，改为描边样式（橙色边框，悬停时填充橙色）
- **分隔线**: 使用虚线分隔符 (`border-top-divider`) 替代原来的 `dotted` 边框
- **滑块样式**: 为 range input 定制了跨浏览器一致的样式，避免 Chromium Linux 上 `accent-color` 渲染 bug
  - 滑轨：4px 高度，左半橙色右半灰色
  - 滑块：14px 圆形橙色
  - 支持 `-webkit` 和 `-moz` 两套伪元素

### 2.3 交互反馈增强

- **按钮操作反馈**: 侧边栏按钮点击后显示 "✓ 已执行" 文本，1 秒后恢复原文字
- **保存按钮反馈**: 保存成功后变为绿色 "完成" 文字，1 秒后恢复
- **清除配置后自动读取**: `wipeConfigHandler()` 完成后自动调用 `readHandler()` 刷新页面状态
- **失焦处理**: 按钮点击后自动 `blur()`，避免持续聚焦状态

### 2.4 Bug 修复

- **Bootloader 按钮修复**: `enterBootloaderHandler()` 参数从 `true` 改为 `null`，修复原版中无效的 bootloader 触发
- **Range 滑块同步**: 添加 `updateRangeFill()` 函数，读取设备数据时同步更新滑块填充指示器

---

## 三、固件 Bug 修复与稳定性改进

### 3.1 范围检查修复 (Off-by-one)

多处将 `>` 修正为 `>=`，防止数组越界：

| 文件 | 修复内容 |
|------|---------|
| `handlers.c:321` | `address > STAGING_IMAGE_SIZE` → `address >= STAGING_IMAGE_SIZE` |
| `hid_report.c:57` | `src->offset > MAX_CC_BUTTONS` → `src->offset >= MAX_CC_BUTTONS` |
| `hid_report.c:73` | `src->offset > MAX_SYS_BUTTONS` → `src->offset >= MAX_SYS_BUTTONS` |
| `usb.c:274` | `idx > MAX_INTERFACES` → `idx >= MAX_INTERFACES` |

### 3.2 数据类型修正

| 文件 | 修复内容 | 影响 |
|------|---------|------|
| `utils.c:82,102` | CRC32 校验值类型从 `uint8_t` 改为 `uint32_t` | 原版截断了 32 位 CRC 值，导致校验可能不准确 |
| `structs.h` | `core1_last_loop_pass` 从 `uint64_t` 改为 `uint32_t` | 与 `time_us_32()` 匹配，避免不必要的 64 位运算 |
| `structs.h` | `last_led_change` 从 `int32_t` 改为 `uint32_t` | 避免时间戳有符号溢出问题 |
| `tasks.c:93` | `last_pointer_move` 从 `int` 改为 `uint32_t` | 类型一致性 |
| `flash.h:50` | `STAGING_IMAGE_SIZE` 宏添加括号 | `(STAGING_PAGES_CNT * FLASH_PAGE_SIZE)` 防止宏展开时运算优先级错误 |

### 3.3 HID 报告解析改进

- **NKRO 回退机制** (`hid_report.c:326`): 当 NKRO 提取失败时（如无线键盘声称支持 NKRO 但实际发送 boot 格式报文），自动回退到标准提取器，而非直接失败
- **Modifier 边界检查** (`hid_report.c:279`): 在 `_extract_kbd_other()` 中添加 `kb->modifier.offset_idx >= len` 的长度检查
- **系统控制报告长度检查** (`keyboard.c:363`): 添加 `length <= SYSTEM_CONTROL_LENGTH` 检查，防止越界读取

### 3.4 复合键盘鼠标跳动修复

- **问题**: QMK 等复合键盘（同时暴露键盘+鼠标 HID 接口）在键盘事件期间会发送零移动的鼠标报告，导致光标跳动
- **修复** (`mouse.c:355`): 在 `process_mouse_report()` 中添加零移动过滤——当 `move_x`、`move_y`、`wheel`、`pan` 全为零且按钮状态未变时，直接 return 不发送报告

### 3.5 macOS 虚拟桌面拖拽修复

- **问题**: 在 macOS 上拖拽窗口跨越虚拟桌面时，相对移动报告会携带按钮状态，导致 HID 鼠标按钮永久"卡住"
- **修复** (`mouse.c:224`): `switch_virtual_desktop_macos()` 中相对移动报告的 `buttons` 强制设为 0

---

## 四、鼠标切换逻辑重构

### 4.1 虚拟桌面切换阈值优化

- **原版**: 所有屏幕切换统一使用 `jump_threshold`，导致虚拟桌面切换也需要跨越较大的阈值间隙
- **本项目**: 新增 `get_jump_threshold()` 函数，区分本地切换和跨设备切换：
  - **本地切换**（虚拟桌面变化）: 阈值为 0，鼠标到达屏幕边缘即可平滑切换
  - **跨设备切换**（跳转到另一台电脑）: 保留 `jump_threshold`，防止误触
  - 判断逻辑基于 `output->screen_index` 和 `output->pos` 方向

### 4.2 零移动过滤

`is_screen_switch_needed()` 中增加 `offset == 0` 的短路判断，避免无意义的计算。

---

## 五、LED 状态管理改进

### 5.1 双状态分离

- **原版**: 单一 `keyboard_leds[]` 数组同时表示期望和实际状态
- **本项目**: 拆分为两个数组：
  - `keyboard_leds_desired[]` — 期望的 LED 状态
  - `keyboard_leds_actual[]` — 实际写入硬件的 LED 状态

### 5.2 LED 同步任务

新增 `led_sync_task()` (`led.c:58`)，以 30Hz 频率检查期望状态与实际状态是否一致，不一致时自动同步。这解决了原版中 LED 状态偶尔不同步的问题。

### 5.3 设置报告成功确认

`set_keyboard_leds()` 中检查 `tuh_hid_set_report()` 的返回值，仅在设置成功时更新 `keyboard_leds_actual`，避免记录未实际生效的状态。

---

## 六、构建系统改进

### 6.1 一键构建脚本 (`build_all.sh`)

新增完整的构建流程脚本，自动化三个步骤：

1. **生成 config.htm**: 调用 `render.py` 打包网页配置
2. **打包磁盘镜像**: 调用 `create.sh` 生成 ramdisk 镜像
3. **编译固件**: cmake 配置 + 编译

**功能特性**:
- 版本号交互输入（记忆上次输入）
- 版本号传递给 CMake (`-DVERSION_MAJOR` / `-DVERSION_MINOR`)
- 彩色终端输出和进度提示
- 构建摘要（固件大小、config.htm 大小等）

### 6.2 CMakeLists.txt 改进

- 版本号支持外部传入（`if(NOT DEFINED ...)`），默认 0.79
- 磁盘镜像依赖声明：`set_source_files_properties(${DISK_ASM} PROPERTIES OBJECT_DEPENDS "${DISK_BIN}")`，确保 disk.img 更新时自动重新编译

### 6.3 .gitignore 完善

扩展忽略规则，新增：
- IDE 配置 (`.vscode/`, `*.swp`)
- OS 文件 (`.DS_Store`, `Thumbs.db`)
- 编译产物 (`*.o`, `*.d`, `*.su`)
- Python 缓存 (`__pycache__/`, `*.pyc`)
- 磁盘镜像中间文件 (`disk/.config_htm_hash`)

---

## 七、PIO USB 稳定性修复

在 `Pico-PIO-USB/src/usb_rx.pio` 中进行了多项 PIO 程序优化：

- **时序调整**: 将 `[2]` 延迟改为 `[1]`，`mov isr, null` 后添加 `[1]` 延迟，优化 NRZI 解码触发时机
- **初始化修复**: `pio_sm_init()` 起始偏移从 `offset + 1` 改为 `offset`，修复状态机初始化位置错误
- **代码清理**: 统一缩进和注释格式

---

## 八、其他改进

### 8.1 USB 描述符修复 (Debug 模式)

- CDC 接口编号修正：普通模式下从 4 改为 2，配置模式使用独立的 `ITF_NUM_CDC_CONFIG = 4`
- 接口总数修正：`ITF_NUM_TOTAL` 从 3 改为 4，`ITF_NUM_TOTAL_CONFIG` 从 5 改为 6
- 配置模式下 CDC 描述符使用正确的接口编号

### 8.2 数据包验证

`utils.c` 的 `validate_packet()` 白名单中添加 `FIRMWARE_UPGRADE_MSG`，允许固件升级消息通过验证。

### 8.3 代码质量

- `pinout.h`: 修正前导空格缩进 (`#define BOARD_ROLE`)
- `misc.h`: 移除未使用的 `crc32()` 函数声明
- RAM 磁盘写入: 提取 `MAX_BLOCK_NO` 常量，提高可读性

### 8.4 资源文件

- 新增 `icon_backup/` 目录：保存原始图标 SVG 文件和转换后的 PNG
- 新增 `movio.uf2` 预编译固件，方便直接刷写测试

---

## 变更影响总结

| 类别 | 变更数量 | 风险等级 |
|------|---------|---------|
| 品牌重塑 | ~15 处 | 低 — 纯文本替换 |
| Web UI 优化 | 6 个文件 | 低 — 前端展示层 |
| Bug 修复 (固件) | 10+ 处 | **高 — 修复了真实缺陷** |
| 鼠标逻辑重构 | 3 处 | 中 — 行为变化需充分测试 |
| LED 管理改进 | 4 处 | 中 — 新增同步任务 |
| 构建系统 | 3 个文件 | 低 — 开发工具链 |
| PIO 修复 | 1 个文件 | 中 — 影响 USB 底层通信 |
