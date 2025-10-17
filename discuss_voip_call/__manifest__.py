{
    "name": "Discuss VoIP Call",
    "version": "1.0",
    "summary": "Add direct VoIP call button in Discuss sidebar",
    "author": "Custom",
    "depends": ["mail", "voip"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "discuss_voip_call/static/src/js/discuss_call.js",
            "discuss_voip_call/static/src/xml/discuss_call.xml",
        ],
    },
    "installable": True,
    "application": False,
}
