""" application configuration """

import os

# application (Flask server) configuration
app = {
    # `debug` is expected to be bool
    "debug": bool(os.getenv("BAEDGE_SERVER_DEBUG", "false")),

    "description": "{Ba,E}dge Computing Server",

    # `dotenv` is expected to be bool
    "dotenv": bool(os.getenv("BAEDGE_SERVER_DOTENV", "false")),

    "fonts": os.getenv("BAEDGE_FONTS_PATH", "./media/fonts"),

    "host": os.getenv("BAEDGE_SERVER_HOST", "0.0.0.0"),

    "logging": {
        # generic logging level, for Baedge functionality etc.
        "level": os.getenv("LOG_LEVEL", "INFO"),

        # Flask-internal logging, primarily for reporting tracebacks and Flask-specific items
        "werkzeug": {
            # `enable` is expected to be bool
            "enable": bool(os.getenv("LOG_WERKZEUG", "false")),

            # Werkzeug-specific log level
            "level": os.getenv("LOG_LEVEL_WERKZEUG", "ERROR"),
        },
    },

    "media": os.getenv("BAEDGE_MEDIA_PATH", "./media"),
    "name": os.getenv("BAEDGE_SERVER_NAME", "🎫 Baedge Server."),

    # define namespaces for routes
    "namespaces": {
        "device": "/device",
        "status": "/status",
    },

    # `port` is expected to be bool
    "port": int(os.getenv("BAEDGE_SERVER_PORT", "2343")),  # `2343` = `BDGE`

    "prefix": "/v1",
    "templates": os.getenv("BAEDGE_TEMPLATES_PATH", "./media/templates"),
}

baedge = {
    "hardware": {
        "model": os.getenv("BAEDGE_HARDWARE_MODEL", "2in9b"),
        "revision": os.getenv("BAEDGE_HARDWARE_REVISION", "_v3"),
    },

    # "1" = 1-bit pixels, black and white, stored with one pixel per byte
    # "L" = 8-bit pixels, grayscale
    # see https://pillow.readthedocs.io/en/latest/handbook/concepts.html#concept-modes
    "image_mode": "1",

    # initial screen to display
    "initial_screen": "baedge",

    # QR code configuration
    "qrcode": {
        # `box_size` defines how many pixels each block of the QR code is
        "box_size": 4,

        # `fit` defines wether the image should be made to fit the bounding box
        "fit": True,

        # `version` is a range between 1 and 40, indicating the size
        "version": 1,
    },

    # (human) wearer-specific configuration
    "wearer": {
        "name": os.getenv("BAEDGE_WEARER_NAME", "{Ba,e}dge"),
        "title": os.getenv("BAEDGE_WEARER_TITLE", "Orchestration at the Edge of Human and Compute."),
        "social": os.getenv("BAEDGE_WEARER_SOCIAL", "@wrklds"),
        "link": os.getenv("BAEDGE_WEARER_LINK", "https://go.workloads.io/baedge"),
    },
}

# media (fonts, images, etc.) configuration
media = {
    "fonts": {
        "isidorasans": app["fonts"] + "/IsidoraSans",
        "robotomono": app["fonts"] + "/RobotoMono",
    },

    "images": {
        "hashicorp_logo": app["media"] + "/images/logomarks/hashicorp/32x32.png",
        "nomad_logo": app["media"] + "/images/logomarks/nomad/32x32.png",
    },

    # files in this dict are served through Flask's `send_from_directory`
    # and do not require the `app["media"]` prefix in their path attribute
    # see https://flask.palletsprojects.com/en/3.0.x/api/#flask.send_from_directory
    "web": {
        "apple-touch-icon": "apple-touch-icon.png",
        "favicon": "favicon.ico",
    },
}

# Nomad environment configuration
nomad = {
    # `NOMAD_ADDR_main` is based on the service name defined in the Nomad Service stanza
    # see https://github.com/workloads/nomad-pack-registry/tree/main/packs/baedge
    "address": os.getenv("NOMAD_ADDR_main", "n/a"),
    "allocation": os.getenv("NOMAD_SHORT_ALLOC_ID", "n/a"),
    "version": os.getenv("NOMAD_VERSION", "n/a"),
}

# application routes for Flask
routes = {
    "root": "/",

    # favicon-like requests
    "apple-touch-icon": "/" + media["web"]["apple-touch-icon"],
    "favicon": "/" + media["web"]["favicon"],

    # /device routes
    "device_clear": app["prefix"] + app["namespaces"]["device"] + "/clear",
    "device_write": app["prefix"] + app["namespaces"]["device"] + "/write",

    # /status routes
    "status": app["prefix"] + app["namespaces"]["status"],
    "status_environment": app["prefix"] + app["namespaces"]["status"] + "/environment",
    "status_routes": app["prefix"] + app["namespaces"]["status"] + "/routes",
    "status_screen": app["prefix"] + app["namespaces"]["status"] + "/screen",
}

# screen configuration
screens = {
    # list of currently active screens
    "active": [
        "baedge",
        "hardware",
        "nomad",
        "socials",
    ],

    # the `socials` screen displays wearer information
    "baedge": {
        "font": {
            "face": media["fonts"]["robotomono"] + "/regular.ttf",
            "size": 15,
        },

        "texts": [
            {
                "content": f'''
                  {app["description"]}

                  go.workloads.io/baedge
                ''',

                "coordinates": (5, 5),
                "fill": 255,
            },
        ]
    },

    # the `socials` screen displays wearer information
    "hardware": {
        "font": {
            "face": media["fonts"]["robotomono"] + "/regular.ttf",
            "size": 15,
        },

        "texts": [
            {
                "content": f'''
                    Model:    {baedge["hardware"]["model"]}
                    Revision: {baedge["hardware"]["revision"]}
                ''',

                "coordinates": (5, 5),
                "fill": 255,
            },
        ]
    },

    # the `nomad` screen displays Nomad-specific information
    "nomad": {
        "font": {
            "face": media["fonts"]["robotomono"] + "/regular.ttf",
            "size": 15,
        },

        "images": [
            {
                "content": media["images"]["hashicorp_logo"],
                "coordinates": (5, 5),
            },
        ],

        "shapes": [
            {
                "coordinates": (32, 0, 750, 31),
                "fill": 0,
                "type": "rectangle",
            },
        ],

        "texts": [
            {
                "content": f'''
                  Allocation ID {nomad["allocation"]}
                  Address:      {nomad["address"]}
                  Version:      {nomad["version"]}
                ''',

                "coordinates": (5, 5),
                "fill": 255,
            }
        ],
    },

    # the `socials` screen displays wearer information
    "socials": {
        "font": {
            "face": media["fonts"]["robotomono"] + "/regular.ttf",
            "size": 15,
        },

        "texts": [
            {
                "content": f'''
                  {baedge["wearer"]["name"]}
                  {baedge["wearer"]["title"]}

                  {baedge["wearer"]["social"]}
                ''',

                "coordinates": (5, 5),
                "fill": 255,
            }
        ],

        "qrcode": {
            "content": baedge["wearer"]["link"],
            "coordinates": (120, 60),
        },
    },
}
