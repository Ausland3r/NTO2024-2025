import re

VALID_FILTERS = {
    "low-pass RC": {"components": ["R", "C"], "type": "RC"},
    "high-pass RC": {"components": ["R", "C"], "type": "RC"},
    "low-pass RL": {"components": ["R", "L"], "type": "RL"},
    "high-pass RL": {"components": ["R", "L"], "type": "RL"}
}

COMPONENT_UNITS = {
    "R": "Ohm",
    "C": "uF",
    "L": "H"
}

COMPONENT_PATTERN = re.compile(r'^(R|C|L)\s*=\s*([0-9]*\.?[0-9]+)\s*(Ohm|uF|H)$', re.IGNORECASE)
W_PATTERN = re.compile(r'^w\s*=\s*([0-9]*\.?[0-9]+)\s*rad/s$', re.IGNORECASE)

ERROR_NO_SUCH_TYPE = "No such type"
ERROR_MISSING_PARAMETERS = "Missing parameters"
ERROR_WRONG_FORMAT = "Wrong format"

def validate_filter_type(filter_type):
    return filter_type in VALID_FILTERS

def parse_parameters(parts):
    components = {}
    w = None

    for part in parts:
        if '=' not in part:
            return ERROR_WRONG_FORMAT, None, None

        key, value = part.split('=', 1)
        key = key.strip()
        value = value.strip()

        if key.lower() == 'w':
            match_w = W_PATTERN.match(part)
            if not match_w:
                return ERROR_WRONG_FORMAT, None, None
            try:
                w_value = float(match_w.group(1))
                if w_value <= 0:
                    return ERROR_WRONG_FORMAT, None, None
                w = w_value
            except:
                return ERROR_WRONG_FORMAT, None, None
        elif key.upper() in COMPONENT_UNITS:
            match_component = COMPONENT_PATTERN.match(part)
            if not match_component:
                return ERROR_WRONG_FORMAT, None, None

            comp = match_component.group(1).upper()
            try:
                value_num = float(match_component.group(2))
                if value_num <= 0:
                    return ERROR_WRONG_FORMAT, None, None
            except:
                return ERROR_WRONG_FORMAT, None, None

            unit = match_component.group(3).lower()
            expected_unit = COMPONENT_UNITS[comp].lower()
            if unit != expected_unit:
                return ERROR_WRONG_FORMAT, None, None

            if comp in components:
                return ERROR_WRONG_FORMAT, None, None

            if comp == 'C':
                value_num *= 1e-6
            components[comp] = value_num
        else:
            return ERROR_WRONG_FORMAT, None, None

    return None, components, w

def calculate_missing_component(filter_type, components, w):
    filter_info = VALID_FILTERS[filter_type]
    required_components = filter_info["components"]
    filter_type_rc_rl = filter_info["type"]

    provided = [comp for comp in required_components if comp in components]
    missing = [comp for comp in required_components if comp not in components]

    if len(missing) > 1:
        return ERROR_MISSING_PARAMETERS

    if len(missing) == 1:
        missing_comp = missing[0]
        try:
            if filter_type_rc_rl == 'RC':
                if missing_comp == 'R':
                    C = components.get('C')
                    if C is None:
                        return ERROR_MISSING_PARAMETERS
                    R = 1 / (w * C)
                    components['R'] = R
                elif missing_comp == 'C':
                    R = components.get('R')
                    if R is None:
                        return ERROR_MISSING_PARAMETERS
                    C = 1 / (w * R)
                    components['C'] = C
            elif filter_type_rc_rl == 'RL':
                if missing_comp == 'R':
                    L = components.get('L')
                    if L is None:
                        return ERROR_MISSING_PARAMETERS
                    R = w * L
                    components['R'] = R
                elif missing_comp == 'L':
                    R = components.get('R')
                    if R is None:
                        return ERROR_MISSING_PARAMETERS
                    L = R / w
                    components['L'] = L
        except:
            return ERROR_WRONG_FORMAT

    elif len(missing) == 0:
        pass
    else:
        return ERROR_MISSING_PARAMETERS

    if not all(comp in components for comp in required_components):
        return ERROR_MISSING_PARAMETERS

    return None

def format_output(filter_type, components, w):
    filter_info = VALID_FILTERS[filter_type]
    required_components = filter_info["components"]

    output_parts = [filter_type]

    if 'C' in required_components:
        C_out = components['C'] / 1e-6
        output_parts.append(f"C = {C_out:.2f} uF")
    elif 'L' in required_components:
        L_out = components['L']
        output_parts.append(f"L = {L_out:.2f} H")

    if 'R' in required_components:
        R_out = components['R']
        output_parts.append(f"R = {R_out:.2f} Ohm")

    output_parts.append(f"w = {w:.2f} rad/s")

    return ", ".join(output_parts)

def parse_input(input_str):
    parts = [part.strip() for part in input_str.split(',')]
    non_empty_parts = [part for part in parts if part]

    if len(non_empty_parts) < 2:
        return ERROR_MISSING_PARAMETERS

    filter_type = non_empty_parts[0]
    if not validate_filter_type(filter_type):
        return ERROR_NO_SUCH_TYPE

    error, components, w = parse_parameters(non_empty_parts[1:])
    if error:
        return error

    if w is None:
        return ERROR_MISSING_PARAMETERS

    error = calculate_missing_component(filter_type, components, w)
    if error:
        return error

    output = format_output(filter_type, components, w)
    return output

def main():
    try:
        input_str = input().strip()
        result = parse_input(input_str)
        print(result)
    except:
        print(ERROR_WRONG_FORMAT)

if __name__ == "__main__":
    main()
