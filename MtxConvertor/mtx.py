from PySide2.QtWidgets import QMainWindow , QPushButton , QWidget  ,QVBoxLayout  ,QLabel
from PySide2.QtCore import *
import hou

class MtxConvertor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.Smain()
        self.SUtils()
        self.Slayout()
        self.Sconnection()

    def Smain(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("MtxConvertor")
        self.setFixedSize(QSize(250,150))
        
    
    def SUtils(self):
        self.coninit_main = QPushButton("Convert & Connect", self)
        # self.Author = QLabel("Autor:- Som Krooz",self)
        # self.Author.setContentsMargins(10, 10, 10, 10)
        self.conbtn = QPushButton("Convert", self)    
    
    def Slayout(self):
        self.verticle = QVBoxLayout()
        self.verticle.setAlignment(Qt.AlignCenter)
        self.Container = QWidget()
        self.Container.setLayout(self.verticle)
        self.verticle.addWidget(self.coninit_main)
        self.verticle.addWidget(self.conbtn)
        # self.verticle.addWidget(self.Author)
        self.setCentralWidget(self.Container)


    def Sconnection(self):
        self.conbtn.clicked.connect(self.convert)
        self.coninit_main.clicked.connect(self.convertConnect)


    def convert(self):
        try:
            selected_nodes = hou.selectedNodes()
            node = selected_nodes[0].path()

            old_mtx = hou.node(node)

            base_color = old_mtx.parm("basecolor_texture").eval()
            roughness = old_mtx.parm("rough_texture").eval()
            normal = old_mtx.parm("baseNormal_texture").eval()
            displacement = old_mtx.parm("dispTex_texture").eval()
            opcaity = old_mtx.parm("opaccolor_texture").eval()

            path = node.split("/")
            new_path = "/".join(path[:-1])

            name = node.split("/")[-1]
            MainPath = hou.node(new_path)  
            subnet = MainPath.createNode("subnet",name)

            surfaceMTX = subnet.createNode("mtlxstandard_surface")
            dispMtx = subnet.createNode("mtlxdisplacement")
            collect = subnet.createNode("collect")

            #DefaultValues
            surfaceMTX.parm("specular_roughness").set(1)
            dispMtx.parm("scale").set("0.01")

            #connect Surface to collect
            collect.setInput(0,surfaceMTX)
            collect.setInput(1,dispMtx)

            
            #Image -- #Matx
            if base_color:
                Base_Color = subnet.createNode("mtlxtiledimage","albedo_map")
                colorCorrect = subnet.createNode("mtlxcolorcorrect","ColorCorrect")
                Base_Color.parm('file').set(base_color)
                colorCorrect.setInput(0,Base_Color)
                surfaceMTX.setInput(1,colorCorrect)    

            if roughness:
                Roughness = subnet.createNode("mtlxtiledimage","roughness_map")
                Roughness.parm("signature").set("Float")
                remap = subnet.createNode("mtlxremap","roughness_remap")
                Roughness.parm('file').set(roughness)
                remap.setInput(0,Roughness)
                surfaceMTX.setInput(6,remap)    
                
            if normal:
                Normal = subnet.createNode("mtlxtiledimage","normal_map")
                normCon = subnet.createNode("mtlxnormalmap")
                normCon.parm("scale").set("0.3")
                
                Normal.parm('file').set(normal)
                normCon.setInput(0,Normal)
                surfaceMTX.setInput(40,normCon)    
                
            if opcaity:
                Opcaity = subnet.createNode("mtlxtiledimage","opacity_map")
                Opcaity.parm('file').set(opcaity)
                surfaceMTX.setInput(38,Opcaity) 

            if displacement:
                Displacement = subnet.createNode("mtlxtiledimage","displacement_map")
                Displacement.parm("signature").set("Float")
                Displacement.parm('file').set(displacement)
                remap = subnet.createNode("mtlxremap","displacement_remap")
                remap.parm('outlow').set(-0.5)
                remap.parm('outhigh').set(0.5)
                remap.setInput(0,Displacement)
                dispMtx.setInput(0,remap)
        except Exception as e:
            print("Error: Select a Node")

        subnet.layoutChildren()
            

    def convertConnect(self):
        try:
            selected_nodes = hou.selectedNodes()
            node = selected_nodes[0].path()

            old_mtx = hou.node(node)

            base_color = old_mtx.parm("basecolor_texture").eval()
            roughness = old_mtx.parm("rough_texture").eval()
            normal = old_mtx.parm("baseNormal_texture").eval()
            displacement = old_mtx.parm("dispTex_texture").eval()
            opcaity = old_mtx.parm("opaccolor_texture").eval()

            path = node.split("/")
            new_path = "/".join(path[:-1])

            name = node.split("/")[-1]
            MainPath = hou.node(new_path)  
            subnet = MainPath.createNode("subnet",name)

            surfaceMTX = subnet.createNode("mtlxstandard_surface")
            dispMtx = subnet.createNode("mtlxdisplacement")
            collect = subnet.createNode("collect")

            #DefaultValues
            surfaceMTX.parm("specular_roughness").set(1)
            dispMtx.parm("scale").set("0.01")

            #connect Surface to collect
            collect.setInput(0,surfaceMTX)
            collect.setInput(1,dispMtx)

            
            #Image -- #Matx
            if base_color:
                Base_Color = subnet.createNode("mtlxtiledimage","albedo_map")
                colorCorrect = subnet.createNode("mtlxcolorcorrect","ColorCorrect")
                Base_Color.parm('file').set(base_color)
                colorCorrect.setInput(0,Base_Color)
                surfaceMTX.setInput(1,colorCorrect)    

            if roughness:
                Roughness = subnet.createNode("mtlxtiledimage","roughness_map")
                Roughness.parm("signature").set("Float")
                remap = subnet.createNode("mtlxremap","roughness_remap")
                Roughness.parm('file').set(roughness)
                remap.setInput(0,Roughness)
                surfaceMTX.setInput(6,remap)    
                
            if normal:
                Normal = subnet.createNode("mtlxtiledimage","normal_map")
                normCon = subnet.createNode("mtlxnormalmap")
                normCon.parm("scale").set("0.3")
                
                Normal.parm('file').set(normal)
                normCon.setInput(0,Normal)
                surfaceMTX.setInput(40,normCon)    
                
            if opcaity:
                Opcaity = subnet.createNode("mtlxtiledimage","opacity_map")
                Opcaity.parm('file').set(opcaity)
                surfaceMTX.setInput(38,Opcaity) 

            if displacement:
                Displacement = subnet.createNode("mtlxtiledimage","displacement_map")
                Displacement.parm("signature").set("Float")
                Displacement.parm('file').set(displacement)
                remap = subnet.createNode("mtlxremap","displacement_remap")
                remap.parm('outlow').set(-0.5)
                remap.parm('outhigh').set(0.5)
                remap.setInput(0,Displacement)
                dispMtx.setInput(0,remap)
            
            
            collect2 = MainPath.createNode("collect",f"OUT")
            collect2.setInput(0,subnet,subnet.outputIndex('surface'))
            collect2.setInput(1,subnet,subnet.outputIndex('displacement'))
            subnet.layoutChildren()

           
        except Exception as e:
            print(e)

