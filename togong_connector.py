## 필요 라이브러리
import bpy
import socket
import threading
import json
## 애드온 메타데이터 입력

bl_info = {
    "name" : "togong connector",
    "author" : "-",
    "version" : (1, 0),
    "blender" : (2, 80, 0),
    "location" : "View3D > Sidebar > TOGONG",
    "description" : "The Addon for connecting togong system",
    "warning" : "",
    "doc_url" : "",
    "category" : "Development"
    }



# 기능구현함수들
def typtext_delete():
    if bpy.context.selected_objects:
        bpy.ops.object.delete()



def typtext_create_topo():
    pass

def typtext_create_pile():
    pass

def typtext_create_heokmakee():
    pass












##서버 관리 클래스
class connection_manager:
    def __init__(self):
        self.server = None
        self.is_running = False
        self.server_thread = None
    
    def start_connection(self):
        if not self.is_running:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(('localhost',9989))
            self.server.listen(5)

            self.server_thread = threading.Thread(target=self.connection_loop)
            self.server_thread.start()

            self.is_running = True

            print("연결됨")
    
    def stop_connection(self):
        if self.is_running:
            self.is_running = False
            self.server.close()
            self.server_thread.join()
            print("연결 끊김")

    def connection_loop(self):
        print("Server listening on localhost:9989")
        while self.is_running:
            try:
                client, address = self.server.accept()
                print(f"Connected with {address}")
                client_thread = threading.Thread(target=handle_client, args=(client,))
                client_thread.start()
            except:
                break


def handle_client(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received: {message}")
                jsonData = json.loads(message)

                typ_text = (jsonData["type"])
                print(typ_text)


                if typ_text == "delete":
                    bpy.app.timers.register(typtext_delete)
                if typ_text == "create_topo":
                    bpy.app.timers.register(typtext_create_topo)                    
                if typ_text == "create_pile":
                    bpy.app.timers.register(typtext_create_pile)
                if typ_text == "create_heokmakee":
                    bpy.app.timers.register(typtext_create_heokmakee)

                    # 변수를 전달해야 할 때
                    #bpy.app.timers.register(lambda: typetext_create_topo("값1", "값2"))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


class start_connection_operator(bpy.types.Operator):
    bl_idname = "togong.connection"
    bl_label = "연결"

    def execute(self, context):
        
        togong_connector.start_connection()
        return {'FINISHED'}

class stop_connection_operator(bpy.types.Operator):
    bl_idname = "togong.disconnection"
    bl_label = "연결끊기"

    def execute(self, context):
        
        togong_connector.stop_connection()
        return {'FINISHED'}

##클래스 정의(UI패널 만들기 기능)
class connection_control_panel(bpy.types.Panel):
    bl_label = "Connection Control"
    bl_idname = "_PT_togong_connection_control"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TOGONG"

    def draw(self, context):
        layout = self.layout

        #연결 상태 표시
        if togong_connector.is_running :

            layout.label(text="연결되었습니다.", icon='CHECKMARK')
        else:
            layout.label(text="연결이 끊겼습니다. 연결하세요.", icon='CANCEL')


        #버튼 생성
        layout.operator(start_connection_operator.bl_idname)
        layout.operator(stop_connection_operator.bl_idname)



##애드온 등록 및 해제 함수

def register():
    bpy.utils.register_class(connection_control_panel)  
    bpy.utils.register_class(start_connection_operator)  
    bpy.utils.register_class(stop_connection_operator)  


def unregister():
    bpy.utils.unregister_class(connection_control_panel)
    bpy.utils.unregister_class(start_connection_operator)  
    bpy.utils.register_class(stop_connection_operator)  


## 애드온 등록
if __name__ == "__main__":
    register()

togong_connector = connection_manager()