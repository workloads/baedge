""" Baedge Configuration """

import os

# application configuration
app = {
  # `debug` is expected to be bool
  "debug": bool(os.getenv("BAEDGE_SERVER_DEBUG", "false")),

  "description": "{Ba,E}dge Computing Server",

  # `dotenv` is expected to be bool
  "dotenv": bool(os.getenv("BAEDGE_SERVER_DOTENV", "false")),

  "host": os.getenv("BAEDGE_SERVER_HOST", "0.0.0.0"),
  "log_level": os.getenv("LOG_LEVEL", "INFO"),
  "media": os.getenv("BAEDGE_MEDIA_PATH", "/opt/baedge-assets/"),
  "name": os.getenv("BAEDGE_SERVER_NAME", "🎫 Baedge Server."),

  # define namespaces for routes
  "namespaces": {
    "device": "/device",
    "status": "/status",
  },

  # `port` is expected to be bool
  "port": int(os.getenv("BAEDGE_SERVER_PORT", "2343")),  # `2343` = `BDGE`

  "prefix": "/v1",
  "templates": os.getenv("BAEDGE_TEMPLATES_PATH", "./templates"),
}

baedge = {
  "screen": {
    "model": os.getenv("BAEDGE_SCREEN_MODEL", "2in9b"),
    "revision": os.getenv("BAEDGE_SCREEN_REVISION", "_v3"),
  },
}

coordinates = {
  # QR code is located in the bottom right corner
  "qrcode": '5, 5'
}

# Baedge environment configuration
# TODO: move to dict?
font_face = os.getenv("BAEDGE_FONT_FACE", "./fonts/RobotoMono/regular.ttf")
font_size = int(os.getenv("BAEDGE_FONT_SIZE", "15"))

# Nomad Environment configuration
nomad = {
    "allocation": os.getenv("NOMAD_SHORT_ALLOC_ID", "n/a"),
    "address": os.getenv("NOMAD_ADDR_http", "n/a"),
    "version": os.getenv("NOMAD_VERSION", "n/a"),
}

media = {
  # favicon-like files are served through Flask's `send_from_directory` and do not need `media` as a prefix
  "apple-touch-icon": 'apple-touch-icon.png',
  "favicon": 'favicon.ico',

  # TODO: find better name for `company_icon`
  "company_icon": app["media"] + 'hashicorp-icon_32x32.png',

  "fonts": {
    # TODO: define fonts
  }
}

# convenience dict for building routes
routes = {
  "root": "/",

  # favicon-like requests
  "apple-touch-icon": "/apple-touch-icon.png",
  "favicon": "/favicon.ico",

  # /device routes
  "device_clear": app["prefix"] + app["namespaces"]["device"] + "/clear",
  "device_write": app["prefix"] + app["namespaces"]["device"] + "/write",

  # /status routes
  "status": app["prefix"] + app["namespaces"]["status"],
  "status_environment": app["prefix"] + app["namespaces"]["status"] + "/environment",
  "status_routes": app["prefix"] + app["namespaces"]["status"] + "/routes",
  "status_screen": app["prefix"] + app["namespaces"]["status"] + "/screen",
}

# (human) wearer configuration
wearer = {
  "name": os.getenv("BAEDGE_WEARER_NAME", "{Ba,e}dge"),
  "title": os.getenv("BAEDGE_WEARER_TITLE", "Orchestration at the Edge of Human and Compute."),
  "social": os.getenv("BAEDGE_WEARER_SOCIAL", "@wrklds"),
  "link": os.getenv("BAEDGE_WEARER_LINK", "https://workloads.io"),
}
