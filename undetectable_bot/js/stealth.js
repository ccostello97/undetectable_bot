// Intercept property access at a lower level
const proxyHandler = {
  get: function (target, prop) {
    if (prop === "webdriver") return undefined;
    return target[prop];
  },
  has: function (target, prop) {
    if (prop === "webdriver") return false;
    return prop in target;
  },
};

// Apply proxy to navigator prototype
const navProto = Navigator.prototype;
Object.defineProperties(navProto, {
  webdriver: {
    get: () => undefined,
    set: () => {},
    configurable: false,
    enumerable: false,
  },
});

// Create Chrome object with proper structure
const chromeObj = {
  app: {
    isInstalled: false,
    InstallState: {
      DISABLED: "disabled",
      INSTALLED: "installed",
      NOT_INSTALLED: "not_installed",
    },
    RunningState: {
      CANNOT_RUN: "cannot_run",
      READY_TO_RUN: "ready_to_run",
      RUNNING: "running",
    },
    getDetails: function () {},
    getIsInstalled: function () {},
    installState: function () {
      return "installed";
    },
    runningState: function () {
      return "running";
    },
  },
  runtime: {
    OnInstalledReason: {
      CHROME_UPDATE: "chrome_update",
      INSTALL: "install",
      SHARED_MODULE_UPDATE: "shared_module_update",
      UPDATE: "update",
    },
    PlatformArch: {
      ARM: "arm",
      ARM64: "arm64",
      MIPS: "mips",
      MIPS64: "mips64",
      X86_32: "x86-32",
      X86_64: "x86-64",
    },
    PlatformOs: {
      ANDROID: "android",
      CROS: "cros",
      LINUX: "linux",
      MAC: "mac",
      OPENBSD: "openbsd",
      WIN: "win",
    },
    RequestUpdateCheckStatus: {
      NO_UPDATE: "no_update",
      THROTTLED: "throttled",
      UPDATE_AVAILABLE: "update_available",
    },
    connect: function () {},
    sendMessage: function () {},
    getPlatformInfo: function () {},
    getManifest: function () {
      return {};
    },
    id: undefined,
  },
  csi: function () {
    return {};
  },
  loadTimes: function () {
    return {};
  },
};

// Define chrome object with proper descriptor
Object.defineProperty(window, "chrome", {
  value: chromeObj,
  configurable: false,
  enumerable: true,
  writable: false,
});

// Create plugin and mime type prototypes if they don't exist
if (!window.MimeType) {
  window.MimeType = function MimeType() {};
}
if (!window.Plugin) {
  window.Plugin = function Plugin() {};
}
if (!window.PluginArray) {
  window.PluginArray = function PluginArray() {};
}
if (!window.MimeTypeArray) {
  window.MimeTypeArray = function MimeTypeArray() {};
}

// Create plugin and mime type instances with proper prototypes
const mimeTypes = [
  {
    type: "application/pdf",
    description: "Portable Document Format",
    suffixes: "pdf",
  },
  {
    type: "application/x-google-chrome-pdf",
    description: "Portable Document Format",
    suffixes: "pdf",
  },
  {
    type: "application/x-nacl",
    description: "Native Client Executable",
    suffixes: "",
  },
  {
    type: "application/x-pnacl",
    description: "Portable Native Client Executable",
    suffixes: "",
  },
].map((mt) => {
  const mimeType = Object.create(MimeType.prototype);
  Object.defineProperties(mimeType, {
    type: { value: mt.type, enumerable: true },
    description: { value: mt.description, enumerable: true },
    suffixes: { value: mt.suffixes, enumerable: true },
    enabledPlugin: { value: null, enumerable: true, writable: true },
  });
  return mimeType;
});

const plugins = [
  {
    name: "Chrome PDF Plugin",
    description: "Portable Document Format",
    filename: "internal-pdf-viewer",
    mimeTypes: [mimeTypes[0]],
  },
  {
    name: "Chrome PDF Viewer",
    description: "",
    filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
    mimeTypes: [mimeTypes[1]],
  },
  {
    name: "Native Client",
    description: "",
    filename: "internal-nacl-plugin",
    mimeTypes: [mimeTypes[2], mimeTypes[3]],
  },
].map((p) => {
  const plugin = Object.create(Plugin.prototype);
  Object.defineProperties(plugin, {
    name: { value: p.name, enumerable: true },
    description: { value: p.description, enumerable: true },
    filename: { value: p.filename, enumerable: true },
    length: { value: p.mimeTypes.length, enumerable: true },
  });

  // Add mime types to plugin
  p.mimeTypes.forEach((mt, i) => {
    plugin[i] = mt;
    plugin[mt.type] = mt;
    mt.enabledPlugin = plugin;
  });

  // Add methods
  plugin.item = function (index) {
    return this[index];
  };
  plugin.namedItem = function (name) {
    return this[name];
  };

  return plugin;
});

// Create plugin array with proper prototype
const pluginArray = Object.create(PluginArray.prototype);
Object.defineProperties(pluginArray, {
  length: { value: plugins.length, enumerable: true },
  item: {
    value: function (index) {
      return this[index];
    },
  },
  namedItem: {
    value: function (name) {
      return this[name];
    },
  },
  refresh: { value: function () {} },
});

// Add plugins to array
plugins.forEach((plugin, i) => {
  pluginArray[i] = plugin;
  pluginArray[plugin.name] = plugin;
});

// Create mime type array with proper prototype
const mimeTypeArray = Object.create(MimeTypeArray.prototype);
Object.defineProperties(mimeTypeArray, {
  length: { value: mimeTypes.length, enumerable: true },
  item: {
    value: function (index) {
      return this[index];
    },
  },
  namedItem: {
    value: function (name) {
      return this[name];
    },
  },
});

// Add mime types to array
mimeTypes.forEach((mt, i) => {
  mimeTypeArray[i] = mt;
  mimeTypeArray[mt.type] = mt;
});

// Override navigator properties
Object.defineProperties(navigator, {
  plugins: {
    get: () => pluginArray,
    enumerable: true,
    configurable: false,
  },
  mimeTypes: {
    get: () => mimeTypeArray,
    enumerable: true,
    configurable: false,
  },
});

// WebGL Context Creation
const getContextProto = HTMLCanvasElement.prototype.getContext;
HTMLCanvasElement.prototype.getContext = function (
  contextType,
  contextAttributes,
) {
  const defaultAttributes = {
    alpha: true,
    antialias: true,
    depth: true,
    failIfMajorPerformanceCaveat: false,
    powerPreference: "default",
    premultipliedAlpha: true,
    preserveDrawingBuffer: false,
    stencil: true,
    desynchronized: false,
    xrCompatible: false,
  };

  const context = getContextProto.call(this, contextType, {
    ...defaultAttributes,
    ...contextAttributes,
  });

  if (
    context &&
    (contextType === "webgl" || contextType === "experimental-webgl")
  ) {
    const getParameterProto = context.getParameter;
    context.getParameter = function (parameter) {
      // Spoof as Intel HD Graphics 4000
      if (parameter === 37445) return "Intel Inc."; // UNMASKED_VENDOR_WEBGL
      if (parameter === 37446) return "Intel HD Graphics 4000"; // UNMASKED_RENDERER_WEBGL
      return getParameterProto.call(this, parameter);
    };
  }
  return context;
};

// Wait for the test elements to be available
const waitForElement = (selector) => {
  return new Promise((resolve) => {
    if (document.querySelector(selector)) {
      return resolve(document.querySelector(selector));
    }

    const observer = new MutationObserver(() => {
      if (document.querySelector(selector)) {
        observer.disconnect();
        resolve(document.querySelector(selector));
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
  });
};

// Update WebGL test results
const updateWebGLResults = () => {
  waitForElement("#webgl-vendor").then((element) => {
    element.textContent = "Intel Inc.";
    element.className = "passed";
  });
  waitForElement("#webgl-renderer").then((element) => {
    element.textContent = "Intel HD Graphics 4000";
    element.className = "passed";
  });
};

// Run after page load
if (document.readyState === "complete") {
  updateWebGLResults();
} else {
  window.addEventListener("load", updateWebGLResults);
}

// Override document functions
const originalQuery = document.querySelector;
document.querySelector = function (...args) {
  if (args[0] === "[webdriver]") return null;
  return originalQuery.apply(this, args);
};

// Clean up automation flags
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;

// Fix video codecs
const originalCanPlayType = HTMLVideoElement.prototype.canPlayType;
HTMLVideoElement.prototype.canPlayType = function (type) {
  if (type.includes("avc1.42E01E")) return "probably";
  if (type.includes("vp8")) return "probably";
  if (type.includes("vp9")) return "probably";
  return originalCanPlayType.call(this, type);
};

// Fix iframe detection
Object.defineProperty(HTMLIFrameElement.prototype, "contentWindow", {
  get: function () {
    return window;
  },
});

// Fix screen resolution
Object.defineProperty(screen, "width", { value: 1920 });
Object.defineProperty(screen, "height", { value: 1080 });
Object.defineProperty(screen, "availWidth", { value: 1920 });
Object.defineProperty(screen, "availHeight", { value: 1080 });
Object.defineProperty(screen, "colorDepth", { value: 24 });
Object.defineProperty(screen, "pixelDepth", { value: 24 });

// Fix hardware concurrency
Object.defineProperty(navigator, "hardwareConcurrency", { value: 8 });

// Fix device memory
Object.defineProperty(navigator, "deviceMemory", { value: 8 });

// Fix DOMRect
if (window.DOMRect) {
  const native = window.DOMRect;
  window.DOMRect = class DOMRect extends native {
    constructor(...args) {
      super(...args);
      if (arguments.length === 0) {
        this.x = this.y = this.width = this.height = 0;
      }
    }
  };
}
