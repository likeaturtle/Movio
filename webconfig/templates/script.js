// ==================== i18n Module ====================
const i18n = {
  currentLang: localStorage.getItem('movio-lang') || 'zh',

  dict: {
    // main.html
    "Oh, no!": "哎呀！",
    "Unfortunately, your browser does not support WebHID or the Permissions Policy is blocking its usage. Please try Chromium \n          (or Chrome if you have to). Apologies for the inconvenience, hopefully a cross-browser solution happens soon.":
      "很遗憾，您的浏览器不支持 WebHID，或权限策略阻止了其使用。请尝试使用 Chromium\n          （或 Chrome）。抱歉造成不便，希望跨浏览器解决方案能尽快实现。",
    "Connect": "连接",
    "Read": "读取",
    "Save": "保存",
    "Exit": "退出",
    "Blink": "闪烁",
    "Blink both": "双闪",
    "Bootloader": "引导模式",
    "Wipe Config": "清除配置",
    "Output A": "输出 A",
    "Output B": "输出 B",
    "Common Config": "通用配置",
    "Device Status": "设备状态",
    "Movio Function Config": "Movio 功能配置",
    "Function Config": "功能配置",

    // form.py field names
    "Running FW version": "当前固件版本",
    "Running FW checksum": "当前固件校验值",
    "Mouse": "鼠标",
    "Force Mouse Boot Mode": "强制鼠标启动模式",
    "Enable Acceleration": "启用加速",
    "Jump Threshold ": "跳转阈值 ",
    "Keyboard": "键盘",
    "Force KBD Boot Protocol": "强制键盘启动协议",
    "KBD LED as Indicator": "键盘 LED 作为状态灯",
    "Enforce Ports": "强制端口",
    "Screen Count": "屏幕数量",
    "Speed X ": "速度 X ",
    "Speed Y ": "速度 Y ",
    "Border Top": "上边界",
    "Border Bottom": "下边界",
    "Operating System": "操作系统",
    "Screen Position": "屏幕位置",
    "Cursor Park Position": "光标停靠位置",
    "Screensaver": "屏幕保护",
    "Mode": "模式",
    "Only If Inactive": "仅不活跃时",
    "Idle Time (μs)": "空闲时间 (μs)",
    "Max Time (μs)": "最大时间 (μs)",

    // Dropdown values
    "Linux": "Linux",
    "MacOS": "MacOS",
    "Windows": "Windows",
    "Android": "Android",
    "Other": "其他",
    "Left": "左",
    "Right": "右",
    "Top": "上",
    "Bottom": "下",
    "Previous": "上次位置",
    "Disabled": "禁用",
    "Pong": "弹球",
    "Jitter": "抖动",
    "None": "无",
    "Backspace": "退格",
    "Caps Lock": "大小写",
    "Tab": "制表",
    "Print Screen": "打印屏幕",
    "Scroll Lock": "滚动锁定",
    "Num Lock": "数字锁定",
  },

  translate(key) {
    if (this.currentLang === 'zh' && this.dict[key]) return this.dict[key];
    return key;
  },

  apply() {
    // Translate elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (el.tagName === 'TITLE') {
        document.title = this.translate(key);
      } else if (el.tagName === 'OPTION') {
        el.textContent = this.translate(key);
      } else if (el.tagName === 'INPUT' && el.type === 'submit') {
        el.value = this.translate(key);
      } else {
        el.textContent = this.translate(key);
      }
    });
    // Sync language switch highlight
    document.querySelectorAll('.lang-opt').forEach(opt => {
      opt.classList.toggle('active', opt.dataset.lang === this.currentLang);
    });
  },

  setLang(lang) {
    this.currentLang = lang;
    localStorage.setItem('movio-lang', this.currentLang);
    this.apply();
  },

  toggle() {
    this.setLang(this.currentLang === 'en' ? 'zh' : 'en');
  },

  init() {
    this.apply();
  }
};

// Apply translations on DOM ready
document.addEventListener('DOMContentLoaded', () => i18n.init());
// ==================== End i18n Module ====================

const mgmtReportId = 6;
var device;

const packetType = {
  keyboardReportMsg: 1, mouseReportMsg: 2, outputSelectMsg: 3, firmwareUpgradeMsg: 4, switchLockMsg: 7,
  syncBordersMsg: 8, flashLedMsg: 9, wipeConfigMsg: 10, readConfigMsg: 16, writeConfigMsg: 17, saveConfigMsg: 18,
  rebootMsg: 19, getValMsg: 20, setValMsg: 21, getValAllMsg: 22, proxyPacketMsg: 23
};

function calcChecksum(report) {
  let checksum = 0;
  for (let i = 3; i < 11; i++)
    checksum ^= report[i];

  return checksum;
}

async function sendReport(type, payload = [], sendBoth = false) {
  if (!device || !device.opened)
    return;

  /* First send this one, if the first one gets e.g. rebooted */
  if (sendBoth) {
    var reportProxy = makeReport(type, payload, true);
    await device.sendReport(mgmtReportId, reportProxy);
    }

    var report = makeReport(type, payload, false);
    await device.sendReport(mgmtReportId, report);
}

function makeReport(type, payload, proxy=false) {
  var dataOffset = proxy ? 4 : 3;
  report = new Uint8Array([0xaa, 0x55, type, ...new Array(9).fill(0)]);

  if (proxy)
    report = new Uint8Array([0xaa, 0x55, packetType.proxyPacketMsg, type, ...new Array(7).fill(0), type]);

  if (payload) {
    report.set([...payload], dataOffset);
    report[report.length - 1] = calcChecksum(report);
  }
  return report;
}

function packValue(element, key, dataType, buffer) {
  const dataOffset = 1;
  var buffer = new ArrayBuffer(8);
  var view = new DataView(buffer);

  const methods = {
    "uint32": view.setUint32,
    "uint64": view.setUint32, /* Yes, I know. :-| */
    "int32": view.setInt32,
    "uint16": view.setUint16,
    "uint8": view.setUint8,
    "int16": view.setInt16,
    "int8": view.setInt8
  };

  if (dataType in methods) {
    const method = methods[dataType];
    if (element.type === 'checkbox')
      view.setUint8(dataOffset, element.checked ? 1 : 0, true);
    else
      method.call(view, dataOffset, element.value, true);
  }

  view.setUint8(0, key);
  return new Uint8Array(buffer);
}

window.addEventListener('load', function () {
  if (!("hid" in navigator)) {
    document.getElementById('warning').style.display = 'block';
  }

  this.document.getElementById('menu-buttons').addEventListener('click', function (event) {
    window[event.target.dataset.handler]();
  })
});

document.getElementById('submitButton').addEventListener('click', async () => { await saveHandler(); });

async function connectHandler() {
  if (device && device.opened)
    return;

  var devices = await navigator.hid.requestDevice({
    filters: [{ vendorId: 0x2e8a, productId: 0x107c, usagePage: 0xff00, usage: 0x10 }]
  });

  device = devices[0];
  device.open().then(async () => {
    device.addEventListener('inputreport', handleInputReport);
    document.querySelectorAll('.online').forEach(element => { element.style.opacity = 1.0; });
    await readHandler();
  });
}

async function blinkHandler() {
  await sendReport(packetType.flashLedMsg, []);
}

async function blinkBothHandler() {
  await sendReport(packetType.flashLedMsg, [], true);
}

function getValue(element) {
  if (element.type === 'checkbox')
    return element.checked ? 1 : 0;
  else
    return element.value;
}

function setValue(element, value) {
  element.setAttribute('fetched-value', value);

  if (element.type === 'checkbox')
    element.checked = value;
  else
    element.value = value;
    element.dispatchEvent(new Event('input', { bubbles: true }));
}


function updateElement(key, event) {
  var dataOffset = 4;
  var element = document.querySelector(`[data-key="${key}"]`);

  if (!element)
    return;

  const methods = {
    "uint32": event.data.getUint32,
    "uint64": event.data.getUint32, /* Yes, I know. :-| */
    "int32": event.data.getInt32,
    "uint16": event.data.getUint16,
    "uint8": event.data.getUint8,
    "int16": event.data.getInt16,
    "int8": event.data.getInt8
  };

  dataType = element.getAttribute('data-type');

  if (dataType in methods) {
    var value = methods[dataType].call(event.data, dataOffset, true);
    setValue(element, value);

    if (element.hasAttribute('data-hex'))
      setValue(element, parseInt(value).toString(16));

    if (element.hasAttribute('data-fw-ver')) {
      /* u16 version = major * 1000 + minor + 100; */
      const major = Math.floor((value - 100) / 1000);
      const minor = (value - 100) % 1000;
      setValue(element, `v${major}.${minor}`);
    }

    /* Range slider: sync fill indicator (range input is sibling, not first in DOM) */
    const rangeEl = document.querySelector(`input.range[data-key="${key}"]`);
    if (rangeEl) updateRangeFill(rangeEl);
  }
}

async function readHandler() {
  if (!device || !device.opened)
    await connectHandler();

  await sendReport(packetType.getValAllMsg);
}

async function handleInputReport(event) {
  var data = new Uint8Array(event.data.buffer);
  var key = data[3];

  updateElement(key, event);
}

async function rebootHandler() {
  await sendReport(packetType.rebootMsg);
}

async function enterBootloaderHandler() {
  await sendReport(packetType.firmwareUpgradeMsg, null, true);
}

async function valueChangedHandler(element) {
  var key = element.getAttribute('data-key');
  var dataType = element.getAttribute('data-type');

  var origValue = element.getAttribute('fetched-value');
  var newValue = getValue(element);

  if (origValue != newValue) {
    uintBuffer = packValue(element, key, dataType);

    /* Send to both devices */
    await sendReport(packetType.setValMsg, uintBuffer, true);

    /* Set this as the current value */
    element.setAttribute('fetched-value', newValue);
  }
}

async function saveHandler() {
  const elements = document.querySelectorAll('.api');

  if (!device || !device.opened)
    return;

  for (const element of elements) {
    var origValue = element.getAttribute('fetched-value')

    if (element.hasAttribute('readonly'))
      continue;

    if (origValue != getValue(element))
      await valueChangedHandler(element);
  }
  await sendReport(packetType.saveConfigMsg, [], true);
}

async function wipeConfigHandler() {
  await sendReport(packetType.wipeConfigMsg, [], true);
}

// ==================== Range slider fill indicator ====================
function updateRangeFill(range) {
  const min = parseFloat(range.min) || 0;
  const max = parseFloat(range.max) || 100;
  const val = parseFloat(range.value) || 0;
  const pct = ((val - min) / (max - min)) * 100;
  range.style.setProperty('--range-fill', pct + '%');
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('input[type="range"].range').forEach(function (range) {
    range.addEventListener('input', function () { updateRangeFill(this); });
    updateRangeFill(range);
  });
});
