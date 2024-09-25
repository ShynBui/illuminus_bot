def remove_local_paths(file_path):
    cleaned_lines = []

    with open(file_path, 'r', encoding='utf-16') as f:
        lines = f.readlines()

    print(lines)

    for line in lines:
        # Kiểm tra xem dòng có chứa '@ file:' hay không
        if '@ file:' not in line:
            # Chỉ giữ lại dòng nếu không chứa '@ file:'
            cleaned_lines.append(line)

    # Ghi kết quả vào file mới hoặc file gốc
    with open(file_path, 'w') as f:
        f.writelines(cleaned_lines)


# Gọi hàm với đường dẫn đến file requirements.txt của bạn
file_path = 'requirements.txt'  # Thay thế bằng đường dẫn thực tế của bạn
remove_local_paths(file_path)

