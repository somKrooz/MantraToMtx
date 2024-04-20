<img src="/icon/mtx.png" width="30%" />
# Plugin for converting mantra materials to materialX <br/>
# Installation

<sub>1 . Copy MtxContertor folder to Houdini<$HOME> scripts/python Folder make sure you have a **__init__.py** file there.</sub><br />
<sub>2 . Open houdini add new tool name it anything you want and on the script tab paste this code.</sub>

---------------------------------------------
    from MtxConvertor import mtx as m
    import importlib

    importlib.reload(m)

    window = m.MtxConvertor()
    window.show()

---------------------------------------------