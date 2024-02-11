""" Baedge Configuration """

import os

# Baedge environment configuration
font_face = os.getenv("BAEDGE_FONT_FACE", "./fonts/RobotoMono/regular.ttf")
font_size = int(os.getenv("BAEDGE_FONT_SIZE", "15"))
screen_model = os.getenv("BAEDGE_SCREEN_MODEL", "2in9b")
screen_revision = os.getenv("BAEDGE_SCREEN_REVISION", "_v3")

# (human) wearer configuration
wearer_name = os.getenv("BAEDGE_WEARER_NAME", "{Ba,e}dge")
wearer_title = os.getenv("BAEDGE_WEARER_TITLE", "Orchestration at the Edge of Human and Compute.")
wearer_social = os.getenv("BAEDGE_WEARER_SOCIAL", "@wrklds")
wearer_link = os.getenv("BAEDGE_WEARER_LINK", "https://workloads.io")

# Nomad Environment configuration
nomad_alloc_id = os.getenv("NOMAD_SHORT_ALLOC_ID", "n/a")
nomad_addr_http = os.getenv("NOMAD_ADDR_http", "http://127.0.0.0")

log_level = os.getenv("LOG_LEVEL", "INFO")

# screen layout configuration
ASSETS_DIR = '/opt/baedge-assets/'

coordinates = {
  # QR code is located in the bottom right corner
  "qrcode": '5, 5'
}

media = {
  "company_icon": ASSETS_DIR + 'hashicorp-icon_32x32.png'
}
