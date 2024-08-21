# FROM quay.io/biocontainers/cellpose:3.0.8
FROM rapidsai/miniforge-cuda:cuda12.5.1-base-ubuntu22.04-py3.12

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY scripts/python/slice_image.py /scripts/slice_image.py
COPY scripts/python/cellpose_seg.py /scripts/cellpose_seg.py
COPY scripts/python/merge_wkts.py /scripts/merge_wkts.py