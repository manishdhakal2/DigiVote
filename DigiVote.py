from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLineEdit,
    QDesktopWidget,
    QMessageBox,
    QScrollArea,
    QDesktopWidget,
    QScrollArea,
)
import sys
from PyQt5.QtGui import QPixmap, QIcon, QImage
import mysql.connector
import os

#----------------------------------------------------------------------------#

class MainAppWindow(QWidget):
    def __init__(self):
        super().__init__()
        background_image = QPixmap("files//main_background.png")
        background_label = QLabel(self)
        background_label.setPixmap(background_image)
        self.setWindowIcon(QIcon("files//App_Icon.png"))

        start_button = QPushButton('VOTE NOW', self)
        button_style = '''
            QPushButton {
                background-color: #826A63;
                color: white;
                border-radius: 30px;
                padding: 12px;
                font-family: sans-serif;
                font-size: 40px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: grey;
            }
        '''
        self.window2=None
        start_button.setStyleSheet(button_style)

        start_button.clicked.connect(self.nextwin)
        start_button.setGeometry(100, 850, 400, 80)  
        

        self.setWindowTitle('DigiVote')
        self.showFullScreen()
        self.setGeometry(0, 0, 1920, 1080)

  #----------------------------------------------------------------------------#
          
    def nextwin(self):
        if not self.window2:
            self.window2=AuthenticationWindow(self)
            self.window2.show()
      
#----------------------------------------------------------------------------#
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

        elif event.key() == Qt.Key_Escape:
            self.close()
        
#----------------------------------------------------------------------------------------------------------------------------------------#
            
class View_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DigiVote")
        self.showFullScreen()
        self.setWindowIcon(QIcon("App_Icon.png"))
        self.setGeometry(0, 0, 1920, 1080)

        self.init_ui()

#----------------------------------------------------------------------------#
    
    def init_ui(self):
        Main_Layout = QVBoxLayout()
        top_section_layout = QHBoxLayout()

        top_label = QLabel("Select One Item/Participant From The Below List")
        top_label.setAlignment(Qt.AlignCenter)
        top_label.setStyleSheet("font-size: 50px;color:#755146; font-weight: bold;")
        self.proceed_button = QPushButton("Vote")
        self.proceed_button.clicked.connect(lambda:self.on_proceed_clicked(self.selected_pname,self.selected_labels))
        self.proceed_button.setStyleSheet("font-size:40px;background-color:grey;color:white;border-radius:40px;width:500px;font-weight:bold;height:80px")
        self.proceed_button.setFixedWidth(300)
        top_section_layout.addWidget(top_label)
        top_section_layout.addWidget(self.proceed_button)
        Main_Layout.addLayout(top_section_layout)
        img_layout = QVBoxLayout()
        row_layout = QHBoxLayout()
        blank_label=QLabel("       \n     \n")
        Main_Layout.addWidget(blank_label)
        self.search_bar=QLineEdit()
        self.search_bar.setStyleSheet("font-family:Helvetica;font-size:20px;border-radius:20px;background-color:#B3B3B3;padding-left:20px")
        self.search_bar.setPlaceholderText("\U0001F50D Enter id/name to search")
        self.search_bar.textChanged.connect(self.search_and_scroll)
        self.search_bar.setFixedSize(600,60)
        
        Main_Layout.addWidget(self.search_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        Main_Layout.setAlignment(Qt.AlignCenter)
        datas = self.opendb()
        self.imgarray = []
        image_box_style='''
        QLabel {
                            font-size:20px;
                            background-color:black;
                            border: 20px solid #826A63;
                            color:white;
                            
        }
        QLabel:hover {
        background-color:grey;
        }
        '''
        self.selected_labels,self.all_labels,self.selected_pname,self.allname,self.all_id=[],[],"",[],[]
        for idx, data in enumerate(datas, start=1):
            img_file = self.blob_to_qimage(data[3])
            img_file = img_file.scaled(400, 300)
            self.imgarray.append(img_file)
            entry_widget = QWidget()

            img_box_label = QLabel(self)
            img_box_label.setPixmap(QPixmap(self.imgarray[-1]))
            img_box_label.setStyleSheet(image_box_style)
            img_id_label=QLabel(f"Id .{data[0]}")
            self.all_id.append(img_id_label)
            img_name_label = QLabel(data[1])
            self.allname.append(img_name_label)
            img_name_label.setAlignment(Qt.AlignCenter)
            img_name_label.setStyleSheet("font-size: 30px;font-weight:bold; color: black;")
            img_id_label.setStyleSheet("font-size: 40px; color: black;font-weight:bold;font-family:Bell MT")
            img_box_label.mousePressEvent = lambda event, label=img_box_label,name=img_name_label: self.label_clicked(event,label,name)
            img_box_label.setFixedWidth(430)
            
            img_box_label.installEventFilter(self)
            img_box_label.setFocus()
            self.all_labels.append(img_box_label)
            entry_layout = QVBoxLayout()
            entry_layout.addWidget(img_box_label)
            entry_layout.addWidget(img_id_label,alignment=Qt.AlignCenter)
            entry_layout.addWidget(img_name_label)
            entry_layout.addSpacing(10)
            entry_widget.setFixedSize(450,400)
            entry_widget.setLayout(entry_layout)
            row_layout.addSpacing(80)
            row_layout.addWidget(entry_widget)
            if idx % 3 == 0:
                img_layout.addLayout(row_layout)
                row_layout = QHBoxLayout()

        if row_layout.count() > 0:
            img_layout.addLayout(row_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(img_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        Main_Layout.addWidget(self.scroll_area)
        self.setLayout(Main_Layout)
    
#----------------------------------------------------------------------------#
    
    def search_and_scroll(self, search_text):
        if not search_text:
            return
        
        for idx, project_name in enumerate(self.allname):
            if search_text.lower() in project_name.text().lower():
                row = idx // 3
                column = idx % 3

                widget = self.allname[idx]

                self.scroll_area.ensureWidgetVisible(widget)

                self.search_bar.setFocus()
                

                break

            for idx, project_name in enumerate(self.all_id):
                if search_text.lower() in project_name.text().lower():
                    row = idx // 3
                    column = idx % 3

                    widget = self.allname[idx]

                    self.scroll_area.ensureWidgetVisible(widget)

                    self.search_bar.setFocus()
                    

                    break
    #------------------------------------------------------------------------------#

            
    def label_clicked(self,event,label,name):


        if label in self.selected_labels:
            label.setStyleSheet('''
                            font-size:20px;
                            backgroun,-color:black;
                            color:white;
                            border:20px solid #826A63;
                            ''')
            self.selected_labels.remove(label)
            self.selected_pname=""
            self.proceed_button.setStyleSheet("font-size:40px;background-color:grey;color:white;border-radius:40px;width:500px;font-weight:bold;height:80px")
        else:
            label.setStyleSheet('''
                            font-size:20px;
                            background-color:black;
                            color:white;
                            border:20px groove blue;
                            ''')
            self.selected_labels.append(label)
            self.selected_pname=name
            if len(self.selected_labels)>1:
                first_lbl=self.selected_labels.pop(0)
                first_lbl.setGraphicsEffect(None)
                self.remove_selection(first_lbl)
            if len(self.selected_labels):
                self.proceed_button.setStyleSheet("font-size:40px;background-color:green;color:white;border-radius:40px;font-weight:bold;width:300px;height:80px")
            else:
                self.proceed_button.setStyleSheet("font-size:40px;background-color:grey;color:white;border-radius:40px;font_weight:bold;width:300px;height:80px")

#----------------------------------------------------------------------------#      

    def remove_selection(self, label):
        
        label.setStyleSheet(''' font-size:20px;
                            background-color:black;
                            color:white;
                            border:20px solid #826A63;
                            ''')
        if len(self.selected_labels)==0:
            self.proceed_button.setStyleSheet("font-size:40px;background-color:grey;color:white;border-radius:40px;width:300px;height:80px")
            
        

 #----------------------------------------------------------------------------#
        
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

#----------------------------------------------------------------------------#
                
    def on_proceed_clicked(self,name,label):
        if(len(label)==0):
            msg=QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setFixedSize(300,300)
            msg.setText("Select At Least One Item")
            msg.setFixedHeight(200)
            msg.setIcon(QMessageBox.Warning)
            x=msg.exec()
            return
        pname=name.text()
        conn=mysql.connector.connect(host=self.open_ip(),user="root",password="swsc1234",database="projectdetails")
        cursor=conn.cursor()
        cursor.execute("UPDATE PROJECT_TABLE SET Vote_Count=Vote_Count+%s WHERE Project_Name=%s",(1,pname))
        conn.commit()
        cursor.close()
        conn.close()
        self.selected_labels[0].setStyleSheet('''
 font-size:20px;
                            background-color:black;
                            color:white;
                            border:20px solid #826A63;
                            border-radius:50px;''')
        self.selected_labels=[]
        self.tq_window=Thanks_Window()
        self.close()
        self.tq_window.show()


    def open_ip(self):
        ip_address="localhost"
        if os.path.exists("files//Server_Ip.txt"):
            with open("files//Server_Ip.txt","r") as filee:
                ip_address=filee.read()
        else:
            ip_address="localhost"
        return ip_address

#----------------------------------------------------------------------------#

    def blob_to_qimage(self, blob):
        qimage = QImage.fromData(blob)
        return qimage
#----------------------------------------------------------------------------#
    
    def opendb(self):
        conn=mysql.connector.connect(host=self.open_ip(),user="root",password="swsc1234",database="projectdetails")
        cursor=conn.cursor()
        cursor.execute("SELECT * From PROJECT_TABLE")

        all_data=cursor.fetchall()
        cursor.close()
        conn.close()
        return all_data

#---------------------------------------------------------------------------------------------------------------------------------------#


 
class AuthenticationWindow(QWidget):
    def __init__(self,MainAppWindow):
        super().__init__()
        self.MainAppWindow=MainAppWindow
        
        self.setWindowTitle("DigiVote")
        self.setWindowIcon(QIcon("App_Icon.ico"))
        
        

        self.init_ui()

    def init_ui(self):
        
        self.setGeometry(600, 800, 400, 200)
        self.center_on_screen()
        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Sunken)
        frame.setStyleSheet("background-color: white; border-radius: 10px;")

        # Create widgets
        enter_votingNo=QLabel("Authentication Page",frame)
        enter_votingNo.setStyleSheet("font-size:55px;color:#755146;font-weight:bold;font-family:helvetica;background-color:transparent")
        blank0=QLabel("\n",frame)
        blank0.setStyleSheet("font-size:55px;color:white;font-weight:bold;font-family:helvetica;background-color:transparent")
        blank1=QLabel("\n",frame)
        blank1.setStyleSheet("font-size:30px;color:white;font-weight:bold;font-family:helvetica;background-color:transparent")
        entry_label = QLineEdit(frame)
        entry_label.setStyleSheet("font-size:20px;font-family:ROBOTO;border-radius:20px;border:3px solid #c68c53;width:90px;height:70px;background-color:rgba(255,255,255,150);padding-left:30px")
        entry_label.setPlaceholderText("\U0001F5DD Identity Card Number")
        
        entry_label.textChanged.connect(lambda:self.color(entry_label))
        self.proceed_button = QPushButton('Proceed', frame)
        self.proceed_button.setStyleSheet("font-size:30px;background-color:grey;border-radius:10px;color:white;font-weight:bold")
        self.proceed_button.setFixedSize(300,50)
        self.proceed_button.clicked.connect(lambda:self.on_proceed_clicked(entry_label))
        frame_layout = QVBoxLayout(frame)
        frame_layout.addWidget(enter_votingNo,alignment=Qt.AlignCenter)
        frame_layout.addWidget(blank0)
        frame_layout.addWidget(entry_label)
        frame_layout.addWidget(blank1)
        frame_layout.addWidget(self.proceed_button,alignment=Qt.AlignCenter)
        frame.setLayout(frame_layout)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame,alignment=Qt.AlignCenter)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
    

    def center_on_screen(self):
        desktop = QDesktopWidget().screenGeometry()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height()) // 2)
    
    def color(self,entry):
        if len(entry.text())==5:
            self.proceed_button.setStyleSheet("font-size:30px;background-color:green;border-radius:10px;color:white;font-weight:bold")
        else:
            self.proceed_button.setStyleSheet("font-size:30px;background-color:grey;border-radius:10px;color:white;font-weight:bold")

    def on_proceed_clicked(self,entry):
        global autharray
        if len(entry.text())!=5:
            msg=QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setFixedSize(300,300)
            msg.setText("Invalid ID Card Number")
            msg.setFixedHeight(200)
            msg.setIcon(QMessageBox.Warning)
            x=msg.exec()
            return
        else:
            if entry.text() in autharray:
                msg=QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setFixedSize(300,300)
                msg.setText("Card Already Used \nUse A Different Card  ")
                msg.setFixedHeight(200)
                msg.setIcon(QMessageBox.Warning)
                x=msg.exec()
                return
            autharray.append(entry.text())
            self.MainAppWindow.close()
            self.close()
            self.window2=View_Window()
            self.window2.show()
        
        


    def center_on_screen(self):
        desktop = QDesktopWidget().screenGeometry()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height()) // 2)
    
    

#---------------------------------------------------------------------------------------------------------------------------------------#



class Thanks_Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thank You")
        self.setGeometry(0,0,1920,1080)
        self.showFullScreen()
        self.setWindowIcon(QIcon("files//App_Icon.png"))
        self.init_ui()
    
    def init_ui(self):
        layout=QHBoxLayout()
        self.bg_img=QPixmap("files//thanks.png")
        self.bg_label=QLabel(self)
        self.bg_label.setPixmap(self.bg_img)
        layout.addWidget(self.bg_label)





        self.setLayout(layout)
        self.delete_ui()

    def delete_ui(self):
        self.Timer=QTimer(self)
        self.Timer.timeout.connect(self.destroy_window)
        self.Timer.timeout.connect(self.gotoMain)
        self.Timer.start(5000)
    
        

    def destroy_window(self):
        
        self.close()
    def gotoMain(self):
        self.window=MainAppWindow()
        self.window.show()
        self.Timer.stop()
    


        
#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#

if __name__ == "__main__":
    global autharray
    autharray=[]
    app = QApplication([])
    window = MainAppWindow()
    window.show()
    sys.exit(app.exec_())
