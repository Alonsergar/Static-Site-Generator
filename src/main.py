from textnode import TextNode,TextType

import os
import shutil
from blocks import markdown_to_html_node,extract_title

def recursive_copy(from_dir,to_dir):
    if not os.path.isdir(from_dir):
        raise ValueError(f"{from_dir} no es un directorio válido")

    os.mkdir(to_dir)

    for item in os.listdir(from_dir):
        src_path = os.path.join(from_dir, item)
        dst_path = os.path.join(to_dir, item)

        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
        elif os.path.isdir(src_path):
            recursive_copy(src_path, dst_path)

def copy_fromD1_toD2(fromDir,toDir):
    
    if not os.path.exists(fromDir):
        raise FileNotFoundError("El directorio origen no existe")

    if os.path.exists(toDir):
        shutil.rmtree(toDir)

    
    recursive_copy(fromDir,toDir)
    #Copy everything recursively

def generate_page(from_path,template_path,dest_path):
   
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
   
    with open(from_path, "r") as f:
        md = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()
    
    
    node = markdown_to_html_node(md)
    html = node.to_html()
    title = extract_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    file_towrite=open(dest_path,'w')
    file_towrite.write(template)
    file_towrite.close()
            



    

def main():
    copy_fromD1_toD2("/home/alonso/Escritorio/Boot.dev/Static-Site-Generator/static","/home/alonso/Escritorio/Boot.dev/Static-Site-Generator/public")
    generate_page("content/index.md","template.html","public/index.html")
    
main()