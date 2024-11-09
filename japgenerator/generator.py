from japgenerator.chars import prefectures, digits, hiragana, veh_types

# Function for license plate livery code generation

def plate_generator(prefecture_type, hiragana_type, veh_type, digits_types):
    dig_code = (prefectures[prefecture_type] + "\n" + hiragana[hiragana_type] + "\n" + veh_types[veh_type] + "\n")
    for i in range(len(digits_types)):
        dig_code += digits[digits_types[i]]["pos"][i]
        dig_code += digits[digits_types[i]]["digit-hex-img"] + "\n"
    return f"""
    FFFF031F000000090009010EFFFFFFFF0009
    <
        FFFF0000000000500054FFA6FFFFFFFF0001
        <
            00020000000002E9018E005AC0C0C0FF0001
            00020000000003150162005AC0C0C0FF0001
            003101B403B2002D00250000C0C0C0FF0007
            0FA5FE640000001100B90000000000190003
            0FA50000039C00110062FFA6070707400005
            0FA5000003B400020054005A0707076B0005
            0FA501D20000000200B200000707076F0003
            0FA5009B0000004200C0FF4C0707071B0001
            0FA5FE800000000800B00000F1F1F17F0001
        >
        0002006A008100160028005A17401CFF0001'
        {dig_code}
    >
        """