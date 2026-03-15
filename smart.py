import tkinter as tk

# 가상 라디오 채널
radio_message = ""

# 전등 상태
led_state = 0
light_mode = 0

# ---------------- 라디오 송신 ----------------
def send_A():
    global radio_message
    radio_message = "A"
    log("송신 → A")
    receive_radio()

def send_B():
    global radio_message
    radio_message = "B"
    log("송신 → B")
    receive_radio()


# ---------------- 라디오 수신 ----------------
def receive_radio():
    global led_state, light_mode

    msg = radio_message
    log(f"수신 ← {msg}")

    if msg == "A":

        light_mode = 0

        if led_state == 0:
            led_state = 1
            led_label.config(text="LED ON", bg="yellow")

        else:
            led_state = 0
            led_label.config(text="LED OFF", bg="gray")

    else:
        light_mode = 1
        led_state = 1
        led_label.config(text="조도 모드", bg="orange")

    update_brightness()


# ---------------- 밝기 계산 ----------------
def update_brightness():
    if light_mode == 1:
        light = light_scale.get()
        brightness = 255 - light
        bright_label.config(text=f"밝기 : {brightness}")
    else:
        bright_label.config(text="밝기 : 수동")


# ---------------- 로그 ----------------
def log(text):
    log_box.insert(tk.END, text + "\n")
    log_box.see(tk.END)


# ---------------- UI ----------------
root = tk.Tk()
root.title("micro:bit 라디오 통신 시뮬레이터")
root.geometry("500x420")

title = tk.Label(root,text="micro:bit Radio Remote Control",font=("Arial",16))
title.pack(pady=10)

# 리모컨
frame_remote = tk.LabelFrame(root,text="리모컨 micro:bit")
frame_remote.pack(fill="x",padx=10,pady=5)

btnA = tk.Button(frame_remote,text="A 버튼",width=10,command=send_A)
btnA.pack(side="left",padx=10,pady=10)

btnB = tk.Button(frame_remote,text="B 버튼",width=10,command=send_B)
btnB.pack(side="left",padx=10,pady=10)


# 전등
frame_light = tk.LabelFrame(root,text="전등 micro:bit")
frame_light.pack(fill="x",padx=10,pady=5)

led_label = tk.Label(frame_light,text="LED OFF",bg="gray",width=20)
led_label.pack(pady=5)

bright_label = tk.Label(frame_light,text="밝기 : 0")
bright_label.pack(pady=5)

light_scale = tk.Scale(frame_light,from_=0,to=255,orient="horizontal",label="조도")
light_scale.pack(fill="x",padx=10)
light_scale.bind("<Motion>",lambda e:update_brightness())


# 로그
log_box = tk.Text(root,height=8)
log_box.pack(fill="both",padx=10,pady=10)

root.mainloop()
