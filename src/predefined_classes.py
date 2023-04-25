# predefined classes
# Daniel Kogan dkogan 114439349
# 04.20.2023

# input
in_class = {
  "type": "class",
  "id_num": 1,
  "children": [
    {
      "scan_int": {
        "type": "method",
        "id_num": 1,
        "return_type": "int",
        "modifiers": [
          "public",
          "static"
        ],
        "children": {}
      }
    },
    {
      "scan_float": {
        "type": "method",
        "id_num": 2,
        "return_type": "float",
        "modifiers": [
          "public",
          "static"
        ],
        "children": {}
      }
    }
  ]
}

# output
out_class = {
  "type": "class",
  "id_num": 2,
  "children": [
    {
      "print": {
        "type": "method",
        "id_num": 3,
        "return_type": "void",
        "modifiers": [
          "public",
          "static"
        ],
        "children": [
          {
            "i": {
              "type": "int",
              "var_type": "field",
              "id_num": 2,
              "return_type": "string",
              "children": {}
            }
          }
        ]
      }
    },
    {
      "print": {
        "type": "method",
        "id_num": 4,
        "modifiers": [
          "public",
          "static"
        ],
        "return_type": "void",
        "children": [
          {
            "i": {
              "type": "float",
              "id_num": 1,
              "id": "i",
              "var_type": "formal"
            }
          }
        ]
      }
    },
    {
      "print": {
        "type": "method",
        "id_num": 5,
        "modifiers": [
          "public",
          "static"
        ],
        "return_type": "void",
        "children": [
          {
            "i": {
              "type": "string",
              "id_num": 1,
              "id": "i",
              "var_type": "formal"
            }
          }
        ]
      }
    },
    {
      "print": {
        "type": "method",
        "id_num": 6,
        "modifiers": [
          "public",
          "static"
        ],
        "return_type": "void",
        "children": [
          {
            "i": {
              "type": "boolean",
              "id_num": 1,
              "id": "i",
              "var_type": "formal"
            }
          }
        ]
      }
    }
  ]
}

class err_class(Exception):
  def __init__(self, msg):
      self.msg = msg
      RED = '\033[91m'
      CLEAR_FORMAT = '\033[0m'
      self.err_msg = f"{RED}ERROR: {CLEAR_FORMAT}{msg}"
      raise Exception(self.err_msg)

  def __str__(self):
      return self.msg
