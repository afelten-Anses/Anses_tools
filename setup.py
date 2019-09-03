#!/usr/bin/env python2

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Anses_tools",
    version="0.1",
    author="Arnaud Felten",
    author_email="arnaud.felten@anses.fr",
    description="Anses_tools ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/afelten-Anses/Anses_tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 2",
        "Operating System :: POSIX :: Linux",
    ],
        scripts=["Magikln.py",
             "cdhit_parser.py",
             "check_Mongo_directories.py",
             "confindr_filterTab.py",
             "contam_filter.py",
             "contam_filter.sh",
             "make_sketch_for_all.py",
             "matrix_to_newick",
             "mongoSave.sh",
             "multiqc_GAMeRdb.sh",
             "redmineSave.sh",
             "roary_to_pairwise"
             ],
    include_package_data=True,
    install_requires=['pymongo',   
                      'confindr',
                      'mash',
                      'dendropy',
                      'multiqc',
                      ], 
    zip_safe=False,

)
