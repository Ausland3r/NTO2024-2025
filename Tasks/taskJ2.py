import re


def parse_input(input_str):
    # Определяем допустимые типы фильтров
    valid_filters = [
        "low-pass RC",
        "high-pass RC",
        "low-pass RL",
        "high-pass RL"
    ]

    # Разбиваем входную строку по запятым
    parts = [part.strip() for part in input_str.split(',')]

    # Удаляем пустые части
    non_empty_parts = [part for part in parts if part]

    if len(non_empty_parts) < 2:
        return "Missing parameters"

    filter_type = non_empty_parts[0]
    if filter_type not in valid_filters:
        return "No such type"

    # Инициализируем значения компонентов и частоты
    components = {}
    w = None

    # Шаблоны для компонентов и частоты
    component_pattern = re.compile(r'^(R|C|L)\s*=\s*([0-9]*\.?[0-9]+)\s*(Ohm|uF|H)$', re.IGNORECASE)
    w_pattern = re.compile(r'^w\s*=\s*([0-9]*\.?[0-9]+)\s*rad/s$', re.IGNORECASE)

    for part in non_empty_parts[1:]:
        if '=' not in part:
            return "Missing parameters"
        key, value = part.split('=', 1)
        key = key.strip()
        value = value.strip()

        # Проверяем, является ли часть частотой
        if key.lower() == 'w':
            match_w = w_pattern.match(part)
            if not match_w:
                return "Wrong format"
            try:
                w_value = float(match_w.group(1))
                if w_value <= 0:
                    return "Wrong format"
                w = w_value
            except:
                return "Wrong format"
        elif key.upper() in ['R', 'C', 'L']:
            match_component = component_pattern.match(part)
            if not match_component:
                return "Wrong format"
            comp = match_component.group(1).upper()
            try:
                value_num = float(match_component.group(2))
                if value_num <= 0:
                    return "Wrong format"
            except:
                return "Wrong format"
            unit = match_component.group(3).lower()
            if comp in components:
                return "Wrong format"
            # Конвертируем в стандартные единицы
            if comp == 'C':
                if unit != 'uf':
                    return "Wrong format"
                value_num *= 1e-6  # uF в F
            elif comp == 'R':
                if unit != 'ohm':
                    return "Wrong format"
                # Ома — стандартная единица
            elif comp == 'L':
                if unit != 'h':
                    return "Wrong format"
                # Генри — стандартная единица
            components[comp] = value_num
        else:
            return "Wrong format"

    # Проверяем, предоставлена ли частота
    if w is None:
        return "Missing parameters"

    # Определяем необходимые компоненты на основе типа фильтра
    if 'RC' in filter_type:
        required_components = ['R', 'C']
    elif 'RL' in filter_type:
        required_components = ['R', 'L']
    else:
        return "No such type"

    # Определяем, какие компоненты предоставлены, а какие отсутствуют
    provided = [comp for comp in required_components if comp in components]
    missing = [comp for comp in required_components if comp not in components]

    # Проверяем, были ли пропущены какие-либо компоненты
    # Также учитываем количество пустых частей, которые могут указывать на пропущенные параметры
    num_provided = len(provided)
    num_required = len(required_components)
    num_missing = num_required - num_provided

    # Если количество предоставленных параметров меньше необходимого, выводим "Missing parameters"
    if num_missing > 1:
        return "Missing parameters"
    elif num_missing == 1:
        missing_comp = missing[0]
        try:
            if 'RC' in filter_type:
                if missing_comp == 'R':
                    C = components.get('C')
                    if C is None:
                        return "Missing parameters"
                    R = 1 / (w * C)
                    components['R'] = R
                elif missing_comp == 'C':
                    R = components.get('R')
                    if R is None:
                        return "Missing parameters"
                    C = 1 / (w * R)
                    components['C'] = C
            elif 'RL' in filter_type:
                if missing_comp == 'R':
                    L = components.get('L')
                    if L is None:
                        return "Missing parameters"
                    R = w * L
                    components['R'] = R
                elif missing_comp == 'L':
                    R = components.get('R')
                    if R is None:
                        return "Missing parameters"
                    L = R / w
                    components['L'] = L
        except:
            return "Wrong format"
    elif num_missing == 0:
        # Все компоненты предоставлены, ничего не вычисляем
        pass
    else:
        return "Missing parameters"

    # Проверяем, все ли необходимые компоненты присутствуют
    if not all(comp in components for comp in required_components):
        return "Missing parameters"

    # Формируем выходную строку
    output_parts = [filter_type]

    if 'C' in required_components:
        C_out = components['C'] / 1e-6  # Конвертируем обратно в uF для вывода
        output_parts.append(f"C = {C_out:.2f} uF")
    elif 'L' in required_components:
        L_out = components['L']
        output_parts.append(f"L = {L_out:.2f} H")

    if 'R' in required_components:
        R_out = components['R']
        output_parts.append(f"R = {R_out:.2f} Ohm")

    output_parts.append(f"w = {w:.2f} rad/s")

    return ", ".join(output_parts)


def main():
    try:
        input_str = input().strip()
        result = parse_input(input_str)
        print(result)
    except Exception as e:
        print("Wrong format")


if __name__ == "__main__":
    main()
