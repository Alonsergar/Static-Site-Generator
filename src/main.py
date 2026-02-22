from textnode import TextNode,TextType

import os
import shutil
from blocks import markdown_to_html_node,extract_title
import sys

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





def generate_page(from_path,template_path,dest_path,basepath):
   
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
    basepath = basepath.rstrip('/')

    template = template.replace('href="/', f'href="{basepath}/')
    template = template.replace('src="/', f'src="{basepath}/')
    
    with open(dest_path,'w') as f:
        f.write(template)


def generate_pages_recursive(dir_path_content,template_path,dest_dir_path,basepath):
    #llamada recursiva para pillar todos los content.md
    for element in os.listdir(dir_path_content):
        dest=os.path.join(dest_dir_path,element)
        path=os.path.join(dir_path_content,element)
        if os.path.isfile(path):
            dest= dest[:-2] + "html"
            generate_page(path,template_path,dest,basepath)
        else:
            
            os.mkdir(dest)
            generate_pages_recursive(path,template_path,dest,basepath)
    




def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    
    copy_fromD1_toD2("/home/alonso/Escritorio/Boot.dev/Static-Site-Generator/static","/home/alonso/Escritorio/Boot.dev/Static-Site-Generator/docs")
    generate_pages_recursive("content/","template.html","docs/",basepath)

main()