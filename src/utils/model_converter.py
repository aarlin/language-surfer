import os
import shutil
import subprocess
import sys
from panda3d.core import Filename, VirtualFileSystem, loadPrcFileData
from direct.showbase.ShowBase import ShowBase

# Create a ShowBase instance for loading models
base = ShowBase()

def convert_to_gltf(input_path, output_path=None):
    """
    Convert a 3D model to glTF format.
    Supports: .obj, .fbx, .dae, .3ds
    
    Args:
        input_path (str): Path to input model file
        output_path (str, optional): Path for output glTF file. 
                                    If None, uses same name as input with .gltf extension
    """
    # Convert paths to absolute paths
    input_path = os.path.abspath(input_path)
    if output_path:
        output_path = os.path.abspath(output_path)
    
    # Set output path if not provided
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + '.gltf'
    
    # Convert the model
    try:
        # Use Blender to convert to glTF
        # First, create a temporary Python script for Blender
        temp_script = os.path.join(os.path.dirname(input_path), 'convert_to_gltf.py')
        with open(temp_script, 'w') as f:
            f.write(f'''
import bpy
import os

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import the model
bpy.ops.import_scene.obj(filepath="{input_path}")

# Export as glTF
bpy.ops.export_scene.gltf(
    filepath="{output_path}",
    export_format='GLTF_SEPARATE',  # Export as separate files
    export_cameras=False,
    export_lights=False,
    export_apply=True
)
''')
        
        # Run Blender in background mode to convert the file
        cmd = ['blender', '--background', '--python', temp_script]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Clean up the temporary script
        os.remove(temp_script)
        
        if result.returncode != 0:
            raise Exception(f"Conversion failed: {result.stderr}")
            
        print(f"Successfully converted {input_path} to {output_path}")
        
        # Copy the original file to models/raw
        raw_dir = os.path.join(os.path.dirname(os.path.dirname(input_path)), "models", "raw")
        os.makedirs(raw_dir, exist_ok=True)
        shutil.copy2(input_path, os.path.join(raw_dir, os.path.basename(input_path)))
        print(f"Copied original file to {raw_dir}")
        
        # Move the glTF files to models/gltf
        gltf_dir = os.path.join(os.path.dirname(os.path.dirname(input_path)), "models", "gltf")
        os.makedirs(gltf_dir, exist_ok=True)
        
        # Move all related files (.gltf, .bin, textures)
        base_name = os.path.splitext(os.path.basename(output_path))[0]
        for ext in ['.gltf', '.bin']:
            src = os.path.join(os.path.dirname(output_path), base_name + ext)
            if os.path.exists(src):
                shutil.move(src, os.path.join(gltf_dir, os.path.basename(src)))
                print(f"Moved {ext} file to {gltf_dir}")
        
        # Move any textures
        textures_dir = os.path.join(gltf_dir, 'textures')
        os.makedirs(textures_dir, exist_ok=True)
        for file in os.listdir(os.path.dirname(output_path)):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                src = os.path.join(os.path.dirname(output_path), file)
                shutil.move(src, os.path.join(textures_dir, file))
                print(f"Moved texture {file} to {textures_dir}")
        
    except Exception as e:
        print(f"Error converting {input_path}: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure Blender is installed and in your PATH")
        print("2. Check if the model file has any material files in the same directory")
        print("3. Try converting the model manually in Blender if needed")
        
def convert_directory(input_dir, output_dir=None):
    """
    Convert all supported models in a directory to glTF format.
    
    Args:
        input_dir (str): Directory containing model files
        output_dir (str, optional): Directory for output glTF files.
                                   If None, uses same directory as input
    """
    input_dir = os.path.abspath(input_dir)
    if output_dir:
        output_dir = os.path.abspath(output_dir)
    else:
        output_dir = input_dir
        
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Supported input formats
    supported_formats = ['.obj', '.fbx', '.dae', '.3ds']
    
    # Convert all supported files
    for filename in os.listdir(input_dir):
        if any(filename.lower().endswith(ext) for ext in supported_formats):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, 
                                     os.path.splitext(filename)[0] + '.gltf')
            convert_to_gltf(input_path, output_path)

if __name__ == "__main__":
    # Convert files in the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    convert_directory(current_dir) 