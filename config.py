""" application configuration """

import os

# application (Flask server) configuration
app = {
    # `debug` is expected to be bool
    "debug": bool(os.getenv("BAEDGE_SERVER_DEBUG", "false")),

    "description": "Compute Server",

    # `dotenv` is expected to be bool
    "load_dotenv": bool(os.getenv("BAEDGE_SERVER_DOTENV", "false")),

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
    "name": os.getenv("BAEDGE_SERVER_NAME", "Baedge"),

    # define namespaces for routes
    "namespaces": {
        "device": "/device",
        "status": "/status",
    },

    # `port` is expected to be bool
    "port": int(os.getenv("BAEDGE_SERVER_PORT", "2343")),  # `2343` = `BDGE`

    "prefix": "/v1",
    "static_files": os.getenv("BAEDGE_STATIC_FILES_PATH", "./media/web"),
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
        "box_size": 3,

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
        "hashicorp_logo": app["media"] + "/images/logomarks/hashicorp/light-32x32.png",
        "nomad_logo": app["media"] + "/images/logomarks/nomad/light-32x32.png",
        "baedge_logo": app["media"] + "/images/logomarks/baedge/light-128x32.png",
        "scale_logo": app["media"] + "/images/logomarks/scale/light-240x66.png"
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
    # list of methods to show in the `status_routes` endpoint
    "visible_methods": [
        "GET",
        "POST",
    ],

    # list of routes to hide from the `status_routes` endpoint
    "hidden_routes": [
        "/<path:filename>",
        "/" + media["web"]["apple-touch-icon"],
        "/" + media["web"]["favicon"],
    ],

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
        "wearer",
        "scale"
    ],

    # the `socials` screen displays wearer information
    "baedge": {
        "font": {
            "face": media["fonts"]["robotomono"] + "/regular.ttf",
            "size": 15,
        },
        "images": [
            {
                "content": media["images"]["baedge_logo"],
                "coordinates": (10, 10),
            },
        ],

        "shapes": [
            {
                "coordinates": (0, 0, 750, 52),
                "fill": 0,
                "type": "rectangle",
            },
        ],
        "texts": [
            {
                "content": app["description"] + "\ngo.workloads.io/baedge",
                "coordinates": (5, 70),
                "fill": 0,
            },
        ]
    },
    "scale": {
        "font": {
            "face": media["fonts"]["robotomono"] + "/regular.ttf",
            "size": 15,
        },

        "images": [
            {
                "content": media["images"]["scale_logo"],
                "coordinates": (15, 55),
            },
        ],
        "shapes": [
            {
                "coordinates": (0, 0, 750, 750),
                "fill": 0,
                "type": "rectangle",
            },
        ],        
    },

    # the `socials` screen displays wearer information
    "hardware": {
        "font": {
            "face": media["fonts"]["robotomono"] + "/regular.ttf",
            "size": 15,
        },
        "images": [
            {
                "content": media["images"]["baedge_logo"],
                "coordinates": (10, 10),
            },
        ],

        "shapes": [
            {
                "coordinates": (0, 0, 750, 52),
                "fill": 0,
                "type": "rectangle",
            },
        ],
        "texts": [
            {
                "content": "Model:    " + baedge["hardware"]["model"] + "\nRevision: " + baedge["hardware"]["revision"],
                "coordinates": (5, 70),
                "fill": 0,
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
                "coordinates": (2, 10),
            },
        ],

        "shapes": [
            {
                "coordinates": (0, 0, 750, 52),
                "fill": 0,
                "type": "rectangle",
            },
        ],

        "texts": [
            {
                "content": "Nomad Runtime",
                "coordinates": (45, 10),
                "fill": 255,
                "font": {
                    "face": media["fonts"]["robotomono"] + "/bold.ttf",
                    "size": 23
                }
            },
            {
                "content": "Allocation ID:" + nomad["allocation"] + "\nAddress:      " + nomad["address"] + "\nVersion:      " + nomad["version"],
                "coordinates": (10, 60),
                "fill": 0,
            }
        ],
    },

    # the `wearer` screen displays wearer information
    "wearer": {
        "font": {
            "face": media["fonts"]["robotomono"] + "/regular.ttf",
            "size": 15,
        },

        "texts": [
            {
                "content": baedge["wearer"]["name"] + "\n" + baedge["wearer"]["title"] + "\n\n" + baedge["wearer"]["social"],  # noqa: E501
                "coordinates": (5, 5),
                "fill": 0,
            }
        ],

        "qrcode": {
            "content": baedge["wearer"]["link"],
            "offset": -0.001
            # "coordinates": (120, 60),
        },
    },
}
