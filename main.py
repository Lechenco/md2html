import markdown
import os

input_path = "./examples/content.md"
output_path = "./build/index.html"
format_vars = {
        "css_styles": "../assets/styles.css"
        }

def readMarkdownFile(file_path: str):
    md_file = ""
    with open(file_path) as file:
        md_file = file.read()

    return extractMetadata(md_file)

def extractMetadata(md_file: str):

    if not md_file.startswith("---"):
        return {}, md_file
    
    end = md_file.index("\n---", 3)
    fm_raw = md_file[3:end].strip()
    content = md_file[end + 4:].lstrip("\n")

    
    metadata = {}
    for line in fm_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition(":")
        metadata[key.strip()] = value.strip()

    return metadata, content

def renderHTML(content: str, metadata: dict):
    html_file = ""
    with open("./templates/example.html", encoding='utf-8') as file:
        html_file = file.read()

    for k in metadata.keys():
        html_file = replacePlaceholder(html_file, "{" + k + "}", metadata[k])
    
    for k in format_vars.keys():
         html_file = replacePlaceholder(html_file, "{" + k + "}", format_vars[k])

    html_file = replacePlaceholder(html_file, "{content}", content)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_file)

def replacePlaceholder(html_body, placeholder, value):
    return html_body.replace(placeholder, value)

def main():
    print("Rendenrizando arquivo HTML")
    metadata, md_file = readMarkdownFile(input_path)
    html_parsed = markdown.markdown(md_file, 
        extensions=['tables', 'fenced_code', 'codehilite'])

    renderHTML(html_parsed, metadata)
    print(f"Html renderizado em {output_path}")

if __name__ == '__main__':
    main()
