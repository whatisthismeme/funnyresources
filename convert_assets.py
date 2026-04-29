
import os
import re
import math
from PIL import Image

# Configuration
SKILL_XML = 'Assets/SkillInfo.xml'
SKILL_DDS_DIR = 'Assets'
STATUS_XML = 'Assets/CharacterCondition.xml'
STATUS_DDS_DIR = 'Assets'
ASSET_DIR = 'Assets'

# Output dirs - mimicking the API structure
# Skill: /res/skillimage/{region}/{id}.png
# Status: /res/status/{id}.png
OUTPUT_BASE = 'static/res'
OUTPUT_SKILL = os.path.join(OUTPUT_BASE, 'skillimage', 'us')
OUTPUT_STATUS = os.path.join(OUTPUT_BASE, 'status')

SKILL_ICON_SIZE = 42
STATUS_ICON_SIZE = 15

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_dds_cache(base_dir):
    cache = {} 
    return cache

def process_skills():
    print(f"Processing Skills from {SKILL_XML}...")
    
    try:
        with open(SKILL_XML, 'rb') as f:
            content = f.read().decode('utf-16')
    except Exception as e:
        print(f"Error reading Skill XML: {e}")
        return

    # Regex to find Skill tags
    # <Skill SkillID="10001" ... ImageFile="data/gfx/image/gui_icon_skill_000.dds" PositionX="2" PositionY="0" ... />
    skill_pattern = re.compile(r'<Skill\s+(.*?)>', re.DOTALL)
    
    # Regex to extract attributes
    attr_pattern = re.compile(r'(\w+)="([^"]*)"')

    count = 0
    dds_cache = {}

    for match in skill_pattern.finditer(content):
        attrs_str = match.group(1)
        attrs = dict(attr_pattern.findall(attrs_str))
        
        skill_id = attrs.get('SkillID')
        image_file = attrs.get('ImageFile')
        
        if not skill_id or not image_file:
            continue

        # Clean image path (remove data/gfx/image/ prefix)
        dds_name = os.path.basename(image_file)
        dds_path = os.path.join(SKILL_DDS_DIR, dds_name)
        
        try:
            pos_x = int(attrs.get('PositionX', 0))
            pos_y = int(attrs.get('PositionY', 0))
        except ValueError:
            # print(f"Skipping Skill {skill_id}: Invalid position data")
            continue

        # Open DDS if not cached
        if dds_path not in dds_cache:
            if os.path.exists(dds_path):
                try:
                    dds_cache[dds_path] = Image.open(dds_path)
                except Exception as e:
                    print(f"Failed to load DDS {dds_path}: {e}")
                    dds_cache[dds_path] = None
            else:
                # print(f"DDS not found: {dds_path}")
                dds_cache[dds_path] = None
                
        img = dds_cache[dds_path]
        if img:
            # Crop
            # Skill: 42x42, 340 width (8 cols), 680 height (16 rows)
            # X Margin: (340 - 8*42)/2 = 2
            # Y Margin: Top align (offset 0) to fix "shifted up" issue
            left = 2 + pos_x * SKILL_ICON_SIZE
            top = 0 + pos_y * SKILL_ICON_SIZE
            right = left + SKILL_ICON_SIZE - 1
            bottom = top + SKILL_ICON_SIZE
            
            # Check bounds
            if right <= img.width and bottom <= img.height:
                icon = img.crop((left, top, right, bottom))
                
                # Save
                # Format: /skillimage/us/{id}.png
                out_path = os.path.join(OUTPUT_SKILL, f"{skill_id}.png")
                
                try:
                    icon.save(out_path, 'PNG')
                    count += 1
                except Exception as e:
                    print(f"Failed to save {out_path}: {e}")
            else:
                print(f"Icon out of bounds for Skill {skill_id}")

    print(f"Processed {count} skills.")

def process_status():
    print(f"Processing Status from {STATUS_XML}...")
    
    try:
        with open(STATUS_XML, 'rb') as f:
            content = f.read().decode('utf-16')
    except Exception as e:
        print(f"Error reading Status XML: {e}")
        return

    # Regex for CharacterCondition
    # <CharacterCondition ConditionID="1" ... ImageFile="..." ... />
    cond_pattern = re.compile(r'<CharacterCondition\s+(.*?)>', re.DOTALL)
    attr_pattern = re.compile(r'(\w+)="([^"]*)"')

    count = 0
    dds_cache = {}
    
    # Ensure status output dir exists
    ensure_dir(OUTPUT_STATUS)

    for match in cond_pattern.finditer(content):
        attrs_str = match.group(1)
        attrs = dict(attr_pattern.findall(attrs_str))
        
        cond_id = attrs.get('ConditionID')
        image_file = attrs.get('ImageFile')
        
        if not cond_id or not image_file:
            continue

        dds_name = os.path.basename(image_file)
        dds_path = os.path.join(STATUS_DDS_DIR, dds_name)
        
        try:
            pos_x = int(attrs.get('PositionX', 0))
            pos_y = int(attrs.get('PositionY', 0))
        except ValueError:
            continue

        if dds_path not in dds_cache:
            if os.path.exists(dds_path):
                try:
                    dds_cache[dds_path] = Image.open(dds_path)
                except Exception as e:
                    print(f"Failed to load DDS {dds_path}: {e}")
                    dds_cache[dds_path] = None
            else:
                dds_cache[dds_path] = None
        
        img = dds_cache[dds_path]
        if img:
            # Status: 15x15, 1px gap including border -> Stride 16
            # Start at 1
            stride = STATUS_ICON_SIZE + 1
            left = 1 + pos_x * stride
            top = 1 + pos_y * stride
            right = left + STATUS_ICON_SIZE
            bottom = top + STATUS_ICON_SIZE
            
            if right <= img.width and bottom <= img.height:
                icon = img.crop((left, top, right, bottom))
                
                # Save
                # Format: /status/{id}.png
                out_path = os.path.join(OUTPUT_STATUS, f"{cond_id}.png")
                
                try:
                    icon.save(out_path, 'PNG')
                    count += 1
                except Exception as e:
                    print(f"Failed to save {out_path}: {e}")

    print(f"Processed {count} statuses.")

def clean_name(name):
    if not name: return ""
    # Remove XML tags or special chars if any. 
    # The user data seems clean but safety first.
    return name.replace('"', '\\"').replace('\n', '')

SKILL_TXT = os.path.join(ASSET_DIR, 'SkillInfo.english.txt')
STATUS_TXT = os.path.join(ASSET_DIR, 'CharacterCondition.english.txt')
ITEM_TXTS = [
    'ItemDB.english.txt', 'itemdb_etc.english.txt', 
    'itemdb_mainequip.english.txt', 'itemdb_subequip.english.txt', 
    'itemdb_weapon.english.txt'
]
ITEM_XMLS = [
    'ItemDB.xml', 'ItemDB_MainEquip.xml', 
    'ItemDB_SubEquip.xml', 'itemDB_ETC.xml', 
    'itemDB_Weapon.xml'
]

def load_txt_map(path):
    mapping = {}
    try:
        with open(path, 'r', encoding='utf-8') as f: # Try utf-8 first, usually these are utf-16 or utf-8
             # The user view showed it as normal text, but let's be robust. 
             # Actually the previous view showed it seemingly utf-8 or ascii compatible.
             # But the XML was utf-16. Text files might be too.
             pass
    except:
        pass
    
    # Let's try flexible loading
    content = ""
    for enc in ['utf-8-sig', 'utf-8', 'utf-16', 'cp949']:
        try:
            with open(path, 'r', encoding=enc) as f:
                content = f.read()
            break
        except:
            continue
            
    for line in content.splitlines():
        parts = line.split('\t')
        if len(parts) >= 2:
            try:
                mapping[parts[0].strip()] = parts[1].strip()
            except:
                pass
    return mapping

def generate_ts_files():
    print("Generating TypeScript name maps using Localized names...")
    
    skill_txt_map = load_txt_map(SKILL_TXT)
    status_txt_map = load_txt_map(STATUS_TXT)
    
    print(f"Loaded {len(skill_txt_map)} skill names and {len(status_txt_map)} status names from stats.")

    # Skills
    skill_map = {}
    try:
        with open(SKILL_XML, 'rb') as f:
            content = f.read().decode('utf-16')
            pattern = re.compile(r'<Skill\s+(.*?)>', re.DOTALL)
            attr_pattern = re.compile(r'(\w+)="([^"]*)"')
            lt_pattern = re.compile(r'_LT\[xml\.skillinfo\.(\d+)\]')
            
            for match in pattern.finditer(content):
                attrs = dict(attr_pattern.findall(match.group(1)))
                sid = attrs.get('SkillID')
                
                # Priority: LocalName -> EngName
                local_ref = attrs.get('SkillLocalName', '')
                name = attrs.get('SkillEngName')
                
                lt_match = lt_pattern.search(local_ref)
                if lt_match:
                    txt_id = lt_match.group(1)
                    if txt_id in skill_txt_map:
                        name = skill_txt_map[txt_id]
                
                if sid and name:
                    skill_map[int(sid)] = clean_name(name)
    except Exception as e:
        print(f"Error parsing skills for TS: {e}")

    # Items
    item_txt_map = {}
    for txt_name in ITEM_TXTS:
        m = load_txt_map(os.path.join(ASSET_DIR, txt_name))
        item_txt_map.update(m)
    print(f"Loaded {len(item_txt_map)} item names from stats.")

    item_map = {}
    for xml_name in ITEM_XMLS:
        try:
            with open(os.path.join(ASSET_DIR, xml_name), 'rb') as f:
                content = f.read().decode('utf-16')
                pattern = re.compile(r'<Mabi_Item\s+(.*?)>', re.DOTALL)
                attr_pattern = re.compile(r'(\w+)="([^"]*)"')
                
                for match in pattern.finditer(content):
                    attrs = dict(attr_pattern.findall(match.group(1)))
                    iid = attrs.get('ID')
                    name = attrs.get('Text_Name0')
                    local_ref = attrs.get('Text_Name1', '')
                    
                    if local_ref:
                        lt_match = re.search(r'(\d+)', local_ref)
                        if lt_match and lt_match.group(1) in item_txt_map:
                            name = item_txt_map[lt_match.group(1)]
                            
                    if iid and name:
                        item_map[int(iid)] = clean_name(name)
        except Exception as e:
            print(f"Error parsing {xml_name} for TS: {e}")

    # Status
    status_map = {}
    try:
        with open(STATUS_XML, 'rb') as f:
            content = f.read().decode('utf-16')
            pattern = re.compile(r'<CharacterCondition\s+(.*?)>', re.DOTALL)
            attr_pattern = re.compile(r'(\w+)="([^"]*)"')
            lt_pattern = re.compile(r'_LT\[xml\.condition\.(\d+)\]') # Hypothetical pattern
            
            for match in pattern.finditer(content):
                attrs = dict(attr_pattern.findall(match.group(1)))
                cid = attrs.get('ConditionID')
                
                local_ref = attrs.get('ConditionLocalName', '')
                name = attrs.get('ConditionEngName')
                
                # Try to map from local name ref
                if local_ref:
                     # Check if it matches _LT pattern
                     lt_match = re.search(r'(\d+)', local_ref)
                     if lt_match and lt_match.group(1) in status_txt_map:
                         name = status_txt_map[lt_match.group(1)]
                elif cid and cid in status_txt_map:
                     # Fallback to direct ID mapping if no LocalName or mapping failed
                     name = status_txt_map[cid]

                if cid and name:
                    status_map[int(cid)] = clean_name(name)
    except Exception as e:
        print(f"Error parsing status for TS: {e}")

    # Write skill.ts
    ensure_dir('src/lib/data')
    with open('src/lib/data/skill.ts', 'w', encoding='utf-8') as f:
        f.write("// Auto-generated by convert_assets.py\n")
        f.write("export const skillNameMap: Record<number, string> = {\n")
        for k, v in sorted(skill_map.items()):
            f.write(f"    {k}: \"{v}\",\n")
        f.write("};\n")
        
    # Write statuscondition.ts
    with open('src/lib/data/statuscondition.ts', 'w', encoding='utf-8') as f:
        f.write("// Auto-generated by convert_assets.py\n")
        f.write("export const statusNameMap: Record<number, string> = {\n")
        for k, v in sorted(status_map.items()):
            f.write(f"    {k}: \"{v}\",\n")
        f.write("};\n")

    # Write item.ts
    with open('src/lib/data/item.ts', 'w', encoding='utf-8') as f:
        f.write("// Auto-generated by convert_assets.py\n")
        f.write("export const itemNameMap: Record<number, string> = {\n")
        for k, v in sorted(item_map.items()):
            f.write(f"    {k}: \"{v}\",\n")
        f.write("};\n")

    print(f"Generated src/lib/data/skill.ts ({len(skill_map)} items)")
    print(f"Generated src/lib/data/statuscondition.ts ({len(status_map)} items)")
    print(f"Generated src/lib/data/item.ts ({len(item_map)} items)")

if __name__ == "__main__":
    ensure_dir(OUTPUT_SKILL)
    ensure_dir(OUTPUT_STATUS)
    process_skills()
    process_status()
    generate_ts_files()
