# XAI Compiler tutorials

XAI follows simple inversion of control (IoC) programming principle to 
allowing user to customize and create use-case-specific explainability report.

This is to increase the modularity of XAI lib and make it easy for extensible.

## Support Format
The supported `external configuration` format are:
* Json - Javascript Object Notation
* Yaml - Rhymes with Camel (converted to Json when loaded)

## Validation
The `external configuration` MUST follow the defined schema bvelow:
```json
      { "definitions": {
            "section": {
                "type": "object",
                "properties": {
                    "title": { "type": "string" },
                    "desc": { "type": "string" },
                    "sections":
                        {
                            "type": "array",
                            "items": { "$ref": "#/definitions/section" },
                            "default": []
                        },
                    "component": { "$ref": "#/definitions/component" }
                },
                "required": ["title"]
            },
            "component": {
                "type": "object",
                "properties": {
                    "package": { "type": "string" },
                    "module": { "type": "string" },
                    "class": { "type": "string" },
                    "attr": {
                        "type": "object"
                    }
                },
                "required": ["class"]
            }
        },

        "type": "object",
        "properties": {
            "name": { "type" : "string" },
            "overview": {" type": "boolean" },
            "content_table": { "type": "boolean" },
            "contents":
                {
                    "type": "array",
                    "items": {"$ref": "#/definitions/section"},
                    "default": []
                },
            "writers":
                {
                    "type": "array",
                    "items": {"$ref": "#/definitions/component"}
                }
        },
        "required": ["name", "content_table", "contents", "writers"]
    }
```
