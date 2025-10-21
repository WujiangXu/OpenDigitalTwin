#!/usr/bin/env python3
"""
Main entry point for OpenDigitalTwin CLI.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli import cli

if __name__ == '__main__':
    cli()
