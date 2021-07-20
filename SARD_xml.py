import xml.etree.ElementTree as ET
import os 

def exclude_header(file_path):
    with open(file_path, 'r') as f:
        code = f.readlines()

    for i in range(len(code)):
        line = code[i]

        if "#include" in code[i]:
            code[i] = f"// {line}"
    
    with open(file_path, 'w') as f:
        f.writelines(code)

def process_mixed(xml_file):
    tree = ET.parse(xml_file)

    root = tree.getroot()

    #* get parent element of all <mixed> elements
    # parent element of <mixed> element is <file> element with a path attribute 
    mixed = root.findall(".//mixed/..")


    count = 0 # count number of mixed files processed

    # for i in range(15):
    for mix in mixed:
        # path = mixed[i].attrib['path']  # 000/
        path = mix.attrib['path']  # 000/
        # print(f"PATH: {path}")

        sub_path, fname = os.path.split(path)
        # print(f"SUB_PATH: {sub_path}")
        # print(f"FNAME: {fname}")

        full_path = os.path.join('SARD', path)  # SARD/000/
        # print(f"FULL_PATH: {full_path}")
        
        if os.path.isfile(full_path):
            output_path = os.path.join('SARD_mixed', sub_path)  # SARD_mixed/000/
            # print(f"OUTPUT_PATH: {output_path}")

            os.makedirs(output_path, exist_ok=True)

            exclude_header(full_path)

            os.system(f"gcc -DOMITBAD -E {full_path} > {output_path}/GOOD_{fname}")
            os.system(f"gcc -DOMITGOOD -E {full_path} > {output_path}/BAD_{fname}")

            count += 1
        # else:
            # print("not in my SARD")
        
        # print("\n\n")
    
    print(f"PROCESSED {count} MIXED FILES")



if __name__ == "__main__":

    process_mixed('SARD_testcaseinfo.xml')

    
    # path = mixed[0].attrib['path']  # 000/
    # print(f"PATH: {path}")

    # sub_path, fname = os.path.split(path)
    # print(f"SUB_PATH: {sub_path}")
    # print(f"FNAME: {fname}")

    # full_path = os.path.join('SARD', path)  # SARD/000/
    # print(f"FULL_PATH: {full_path}")

    # if os.path.isfile(full_path):
    #     output_path = os.path.join('SARD_mixed', sub_path) # SARD_mixed/000/
    #     print(f"OUTPUT_PATH: {output_path}")

    #     os.makedirs(output_path, exist_ok=True)

    #     exclude_header(full_path) 

    #     os.system(f"gcc -DOMITBAD -E {full_path} > {output_path}/GOOD_{fname}")
    #     os.system(f"gcc -DOMITGOOD -E {full_path} > {output_path}/BAD_{fname}")
    # else:
    #     print("not in my SARD")




    # # /000/
    # path1 = mixed[10].attrib['path']
    # print(path1)

    # path0, fname = os.path.split(path1)
    # print(path0)

    # # SARD/000/
    # path2 = os.path.join('SARD', path1)
    # print(path2)



    # #* check if mixed file exists (not all of them do)
    # if os.path.isfile(path2):
    #     print("yes!")
    # else:
    #     print("no")


    # #* output file path
    # # SARD_mixed/000/
    # path3 = os.path.join('SARD_mixed', path0)
    # print(path3)

    # os.makedirs(path3, exist_ok=True) 

    # os.system(f"gcc -DOMITBAD -E {path2} > {path3}/{fname}")