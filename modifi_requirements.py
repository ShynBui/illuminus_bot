import os
import xml.etree.ElementTree as ET


def print_folder_structure(element, indent=""):
    if element.tag == 'Folder':
        # In tên thư mục với định dạng: Thư mục/
        print(f"{indent}{element.attrib['name']}/")
        indent += "    "  # Tăng khoảng trắng cho thư mục con
        for child in element:
            print_folder_structure(child, indent)
    elif element.tag == 'File':
        # In tên file với định dạng: Tệp
        print(f"{indent}{element.attrib['name']}")

def parse_and_print_xml(file_path):
    # Phân tích tệp XML
    tree = ET.parse(file_path)
    root = tree.getroot()
    # In cấu trúc thư mục
    print_folder_structure(root)

def create_xml_for_folder(folder_path, parent_element):
    # Duyệt qua tất cả các tệp và thư mục trong thư mục hiện tại
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path):
            # Nếu là thư mục, tạo một element folder
            folder_element = ET.SubElement(parent_element, 'Folder', name=item)
            # Đệ quy để thêm các thư mục con và tệp
            create_xml_for_folder(item_path, folder_element)
        else:
            # Nếu là tệp, tạo một element file
            file_element = ET.SubElement(parent_element, 'File', name=item)


def generate_folder_xml(folder_path, output_file):
    # Tạo phần gốc (root) của tệp XML
    root = ET.Element('FolderStructure')
    # Bắt đầu tạo XML từ thư mục
    create_xml_for_folder(folder_path, root)
    # Tạo cây XML và ghi ra tệp
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

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


if __name__ == "__main__":
    # Gọi hàm với đường dẫn đến file requirements.txt của bạn
    # file_path = 'requirements.txt'  # Thay thế bằng đường dẫn thực tế của bạn
    # remove_local_paths(file_path)
    #
    folder_path = r"D:\illuminus_bot"
    #
    output_file = "folder_structure.xml"

    # Gọi hàm để tạo XML
    generate_folder_xml(folder_path, output_file)

    parse_and_print_xml(output_file)
