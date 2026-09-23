#!/usr/bin/env python3
"""Validate the implemented 1776 world against the authoritative V2 target.

The destructive redistribution is intentionally kept in
``build_start_1776_world_apply.py`` behind its explicit ``--apply`` flag.
This stable entry point performs the complete post-implementation validation
against BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE_V2.csv.
"""

from __future__ import annotations

from build_start_1776_final_validate import main


if __name__ == "__main__":
    main()
