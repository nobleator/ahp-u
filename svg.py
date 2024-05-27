def find_longest_string(dictionary):
    max_length = 0
    for key in dictionary.keys():
        for word in key.split(' '):
            if len(word) > max_length:
                max_length = len(word)
    for value_list in dictionary.values():
        for value in value_list:
            for word in value.split(' '):
                if len(word) > max_length:
                    max_length = len(word)
    return max_length

def wrap_text(text, max_line_length, init_x, init_y):
    wrapped_text = []
    y = init_y  # Initial y-coordinate
    while len(text) > max_line_length:
        # Find the last space before the maximum line length
        last_space_index = text.rfind(' ', 0, max_line_length)
        if last_space_index == -1:
            # If no space found within max_line_length, break the word
            last_space_index = max_line_length
        # Append the wrapped line with x and y attributes to the list
        wrapped_text.append(f'<text x="{init_x}em" y="{y}em" text-anchor="middle" alignment-baseline="middle">{text[:last_space_index]}</text>')
        # Increment y for the next line
        y += 1
        # Remove the wrapped part from the original text
        text = text[last_space_index+1:]
    # Append the remaining text with x and y attributes
    wrapped_text.append(f'<text x="{init_x}em" y="{y}em" text-anchor="middle" alignment-baseline="middle">{text}</text>')
    return wrapped_text

def generate_svg(data):
    # Calculate dimensions and positions
    box_width = find_longest_string(data)
    box_height = 3
    margin_x = 1
    margin_y = 1
    nest_offset = box_width / 3
    horizontal_spacing = 1

    svg_content = ""
    
    total_height = sum((len(v)) * (box_height) for v in data.values())
    total_width = margin_x * 0.5 + len(data) * box_width + (len(data) - 1) * horizontal_spacing + 1
    svg_content += f'<svg width="{total_width}em" height="{total_height}em" xmlns="http://www.w3.org/2000/svg">'
    x_offset_parent = margin_x
    for key, values in data.items():
        y_offset = margin_y
        svg_content += f'<rect x="{x_offset_parent}em" y="{y_offset}em" width="{box_width}em" height="{box_height}em" fill="#4a90e2" stroke="black" />'
        lines = wrap_text(key, box_width, x_offset_parent + box_width / 2, y_offset + box_height / 2)
        for line in lines:
            svg_content += line

        x_offset_child = x_offset_parent + nest_offset
        for i, value in enumerate(values):
            y_offset_child = y_offset + (i + 1) * (box_height + margin_y)  # Adjust child box y-coordinate
            svg_content += f'<rect x="{x_offset_child}em" y="{y_offset_child}em" width="{2 * box_width / 3}em" height="{box_height}em" fill="#4a90e2" stroke="black" />'
            lines = wrap_text(value, box_width, x_offset_child + box_width / 3, y_offset_child + box_height / 2)
            for line in lines:
                svg_content += line

            # Draw lines connecting key box and value box
            svg_content += f'<line x1="{x_offset_parent + box_width * 0.25}em" y1="{y_offset + box_height}em" x2="{x_offset_parent + box_width * 0.25}em" y2="{y_offset_child + box_height / 2}em" stroke="black" />'  # Line from key to bend
            svg_content += f'<line x1="{x_offset_parent + box_width * 0.25}em" y1="{y_offset_child + box_height / 2}em" x2="{x_offset_child}em" y2="{y_offset_child + box_height / 2}em" stroke="black" />'  # Line from bend to value

        x_offset_parent += box_width + horizontal_spacing  # Adjust x_offset for next key

    svg_content += '</svg>'

    return svg_content