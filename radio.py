import tkinter as tk

# 가상 라디오 채널
radio_value = 0

# 송신기 전송수
send_count = 0


# ---------------- 송신 ----------------
def press_A():
    global send_count, radio_value
    send_count += 1
    radio_value = send_count
    
    label_send.config(text=f"전송수 : {send_count}")
    log.insert(tk.END, f"송신 → {radio_value}\n")
    
    receive_radio()


def press_B():
    global send_count, radio_value
    send_count = 0
    radio_value = 0
    
    label_send.config(text="전송수 : 0")
    label_recv.config(text="수신수 : 0")
    label_cal.config(text="칼로리 : 0")
    
    log.insert(tk.END, "초기화\n")


# ---------------- 수신 ----------------
def receive_radio():
    recv = radio_value
    calories = recv * 0.32
    
    label_recv.config(text=f"수신수 : {recv}")
    label_cal.config(text=f"수신수 × 0.32 = {calories:.2f}")


# ---------------- UI ----------------
root = tk.Tk()
root.title("micro:bit 라디오 송수신 TK 시뮬레이터")
root.geometry("500x350")

title = tk.Label(root,text="micro:bit Radio Simulator",font=("Arial",16))
title.pack(pady=10)


# 송신기
frame_tx = tk.LabelFrame(root,text="micro:bit 송신기")
frame_tx.pack(fill="x",padx=10,pady=5)

label_send = tk.Label(frame_tx,text="전송수 : 0",font=("Arial",12))
label_send.pack(pady=5)

btnA = tk.Button(frame_tx,text="A 버튼 (전송 +1)",width=20,command=press_A)
btnA.pack(pady=3)

btnB = tk.Button(frame_tx,text="B 버튼 (초기화)",width=20,command=press_B)
btnB.pack(pady=3)


# 수신기
frame_rx = tk.LabelFrame(root,text="micro:bit 수신기")
frame_rx.pack(fill="x",padx=10,pady=5)

label_recv = tk.Label(frame_rx,text="수신수 : 0",font=("Arial",12))
label_recv.pack(pady=5)

label_cal = tk.Label(frame_rx,text="수신수 × 0.32 = 0",font=("Arial",12))
label_cal.pack(pady=5)


# 로그
log = tk.Text(root,height=8)
log.pack(fill="both",padx=10,pady=10)


root.mainloop()
