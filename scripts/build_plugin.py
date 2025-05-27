"""Build script for creating the .zxp installer."""

import os
import shutil
import subprocess
import json
from pathlib import Path
import zipfile


def build_plugin():
    """Build the FPV Transition plugin."""
    print("Building FPV Transition Plugin...")
    print("="*50)
    
    # Create build directory
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    
    # Create plugin structure
    plugin_dir = build_dir / "FPVTransition"
    plugin_dir.mkdir(exist_ok=True)
    
    # Copy CEP panel files
    print("Copying CEP panel files...")
    cep_source = Path("src/cep-panel")
    cep_dest = plugin_dir / "CSXS"
    shutil.copytree(cep_source, cep_dest, dirs_exist_ok=True)
    
    # Create manifest.xml
    print("Creating manifest.xml...")
    create_manifest(cep_dest)
    
    # Copy ExtendScript files
    print("Copying ExtendScript files...")
    jsx_source = Path("src/extendscript")
    jsx_dest = plugin_dir / "jsx"
    shutil.copytree(jsx_source, jsx_dest, dirs_exist_ok=True)
    
    # Copy Python backend
    print("Copying Python backend...")
    backend_source = Path("src")
    backend_dest = plugin_dir / "backend"
    shutil.copytree(backend_source, backend_dest, dirs_exist_ok=True)
    
    # Copy configuration
    shutil.copy("config/default.json", plugin_dir / "config.json")
    
    # Create startup script
    create_startup_script(plugin_dir)
    
    # Package as ZXP
    print("\nPackaging as ZXP...")
    zxp_path = build_dir / "FPVTransition_v1.0.0.zxp"
    
    # Use ZXPSignCmd if available, otherwise create ZIP
    if shutil.which("ZXPSignCmd"):
        subprocess.run([
            "ZXPSignCmd", "-selfSignedCert", "NA", "NA", "NA", "NA", "NA",
            str(zxp_path)
        ], cwd=str(plugin_dir))
    else:
        print("ZXPSignCmd not found, creating unsigned ZIP...")
        with zipfile.ZipFile(zxp_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(plugin_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(plugin_dir)
                    zf.write(file_path, arc_path)
    
    print(f"\n✅ Build complete! Plugin saved to: {zxp_path}")
    print("\nInstallation instructions:")
    print("1. Install using ZXP/UXP Installer or Adobe Exchange")
    print("2. Restart Premiere Pro")
    print("3. Find the plugin in Window > Extensions > FPV Transitions")


def create_manifest(cep_dir):
    """Create CEP manifest.xml."""
    manifest_content = '''<?xml version="1.0" encoding="UTF-8"?>
<ExtensionManifest Version="10.0" ExtensionBundleId="com.mauriale.fpvtransition" 
                   ExtensionBundleVersion="1.0.0" 
                   ExtensionBundleName="FPV Transition Plugin">
    <ExtensionList>
        <Extension Id="com.mauriale.fpvtransition.panel" Version="1.0.0"/>
    </ExtensionList>
    <ExecutionEnvironment>
        <HostList>
            <Host Name="PPRO" Version="[23.0,99.9]"/>
        </HostList>
        <LocaleList>
            <Locale Code="All"/>
        </LocaleList>
        <RequiredRuntimeList>
            <RequiredRuntime Name="CSXS" Version="10.0"/>
        </RequiredRuntimeList>
    </ExecutionEnvironment>
    <DispatchInfoList>
        <Extension Id="com.mauriale.fpvtransition.panel">
            <DispatchInfo>
                <Resources>
                    <MainPath>./index.html</MainPath>
                    <ScriptPath>./jsx/fpv_effects.jsx</ScriptPath>
                </Resources>
                <Lifecycle>
                    <AutoVisible>true</AutoVisible>
                </Lifecycle>
                <UI>
                    <Type>Panel</Type>
                    <Menu>FPV Transitions</Menu>
                    <Geometry>
                        <Size>
                            <Height>600</Height>
                            <Width>400</Width>
                        </Size>
                    </Geometry>
                </UI>
            </DispatchInfo>
        </Extension>
    </DispatchInfoList>
</ExtensionManifest>
'''
    
    manifest_path = cep_dir / "manifest.xml"
    manifest_path.write_text(manifest_content)


def create_startup_script(plugin_dir):
    """Create startup script for backend server."""
    startup_content = '''#!/usr/bin/env python
"""Startup script for FPV Transition backend server."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.backend.server import app

if __name__ == "__main__":
    print("Starting FPV Transition Backend Server...")
    print("Server running at http://localhost:8080")
    app.run(host="0.0.0.0", port=8080)
'''
    
    startup_path = plugin_dir / "start_server.py"
    startup_path.write_text(startup_content)
    
    # Create batch file for Windows
    batch_content = '''@echo off
python start_server.py
pause
'''
    
    batch_path = plugin_dir / "start_server.bat"
    batch_path.write_text(batch_content)


if __name__ == "__main__":
    build_plugin()