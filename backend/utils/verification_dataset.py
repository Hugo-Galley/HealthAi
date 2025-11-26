import pandas as pd

def try_parse_value(value, intended_type):
        match intended_type:
            case "int":
                try:
                    int(float(value))
                    return True
                except (ValueError, TypeError):
                    return False
            case "float":
                try:
                    float(value)
                    return True
                except (ValueError, TypeError):
                    return False
            case "str":
                return isinstance(value, str)
            case _:
                return False
            
def find_non_parse_type(df: pd.DataFrame, item_type):
    non_parse = []
    for line in range(df.shape[0]):
        for item, intended_type in item_type.items():
            value = df.loc[line, item]
            if value == "" or pd.isna(value):
                continue
            elif not try_parse_value(value, intended_type):
                non_parse.append(
                    {"line": line + 1, "field_value": item, "attempt_type": intended_type, "value": value})
    return {"findError": non_parse}
