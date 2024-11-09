from japgenerator.chars import prefectures, hiragana, veh_types

generation_stages = [
    {
    "datatype": "prefecture",
    "kb-array": prefectures.keys(),
    "reply_text": "Choose prefecture"
    },
    {
    "datatype": "hiragana",
    "kb-array": hiragana.keys(),
    "reply_text": "Choose hiragana"
    },
    {
    "datatype": "veh_type",
    "kb-array": veh_types.keys(),
    "reply_text": "Choose vehicle type"
    },
    {
    "datatype": "digits",
    "kb-array": None,
    "reply_text": "Type four digits for a plate"
    },
]