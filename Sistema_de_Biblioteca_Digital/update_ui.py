import os
import glob
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Headers
    content = content.replace('<div class="d-flex justify-content-between align-items-center mb-4">', '<div class="page-header align-items-end mb-4">')
    content = content.replace('<h2>', '<h1 class="fw-extrabold text-dark mb-1">')
    content = content.replace('</h2>', '</h1>')

    # Cards to Panels
    content = content.replace('<div class="card shadow">', '<div class="panel border-0 shadow-sm table-panel mt-4">')
    content = content.replace('<div class="card-body">', '<div class="panel-body">')
    content = content.replace('<div class="card">', '<div class="panel border-0 shadow-sm">')

    # Forms
    content = content.replace('class="form-control"', 'class="form-control bg-light"')
    content = content.replace('class="form-select"', 'class="form-select bg-light"')

    # Charts in dashboard
    if 'dashboard' in filepath:
        content = content.replace('height: 300px;', 'height: 220px;')
        content = content.replace('height: 280px;', 'height: 200px;')
        content = content.replace('height: 260px;', 'height: 200px;')

    # Save if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {filepath}')

files = glob.glob('**/*.html', recursive=True)
for f in files:
    if 'templates' in f:
        process_file(f)
