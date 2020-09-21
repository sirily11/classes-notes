from docs_generator.docs_generator import convert_notebook_to_html
from shutil import copytree

if __name__ == '__main__':
    convert_notebook_to_html(site_name="Class Notes")
    print("Copy index.md")
    with open('README.md', 'r') as f:
        content = f.read()
        with open('docs/index.md', 'w') as f1:
            f1.write(content)