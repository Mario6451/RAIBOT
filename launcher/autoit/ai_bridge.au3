#include <Array.au3>
#include <JSON.au3>

; ============================================================
; CONFIG
; ============================================================
Global $HTTP_URL = "http://127.0.0.1:5005/command"
Global $TCP_HOST = "127.0.0.1"
Global $TCP_PORT = 5006
Global $CMD_FILE = "botcmd.txt"

TCPStartup()
Global $tcp_socket = -1


; ============================================================
; MAIN LOOP
; ============================================================
While 1
    ; 1) Try HTTP
    If _TryHTTP() Then
        Sleep(10)
        ContinueLoop
    EndIf

    ; 2) Try TCP
    If _TryTCP() Then
        Sleep(10)
        ContinueLoop
    EndIf

    ; 3) Fallback to file
    _TryFile()

    Sleep(10)
WEnd



; ============================================================
; HTTP COMMAND HANDLER
; ============================================================
Func _TryHTTP()
    Local $data = InetRead($HTTP_URL, 1)
    If @error Or BinaryLen($data) = 0 Then Return False

    Local $json = BinaryToString($data)
    Return _ProcessJSON($json)
EndFunc



; ============================================================
; TCP COMMAND HANDLER
; ============================================================
Func _TryTCP()
    Local $sock = TCPConnect($TCP_HOST, $TCP_PORT)
    If $sock = -1 Then Return False

    Local $data = TCPRecv($sock, 4096)
    TCPCloseSocket($sock)

    If $data = "" Then Return False

    Return _ProcessJSON($data)
EndFunc



; ============================================================
; FILE COMMAND HANDLER
; ============================================================
Func _TryFile()
    If Not FileExists($CMD_FILE) Then Return False

    Local $data = FileRead($CMD_FILE)
    If $data = "" Then Return False

    Return _ProcessJSON($data)
EndFunc



; ============================================================
; JSON COMMAND PROCESSOR
; ============================================================
Func _ProcessJSON($json)
    Local $obj = _JSON_Parse($json)
    If @error Then Return False

    Local $cmd = $obj.cmd

    Switch $cmd

        ; ----------------------------------------------------
        ; MOUSE MOVEMENT
        ; ----------------------------------------------------
        Case "mouse_abs"
            MouseMove($obj.x, $obj.y, $obj.speed)

        Case "mouse_delta"
            DllCall("user32.dll", "none", "mouse_event", _
                "dword", 0x0001, _
                "dword", $obj.dx, _
                "dword", $obj.dy, _
                "dword", 0, _
                "ptr", 0)

        ; ----------------------------------------------------
        ; MOUSE BUTTONS
        ; ----------------------------------------------------
        Case "right_down"
            MouseDown("right")

        Case "right_up"
            MouseUp("right")

        Case "left_click"
            MouseClick("left")

        ; ----------------------------------------------------
        ; KEYBOARD
        ; ----------------------------------------------------
        Case "key_down"
            Send("{" & $obj.key & " down}")

        Case "key_up"
            Send("{" & $obj.key & " up}")

        ; ----------------------------------------------------
        ; SLEEP
        ; ----------------------------------------------------
        Case "sleep"
            Sleep($obj.ms)

        ; ----------------------------------------------------
        ; ATTACK-MOVE
        ; ----------------------------------------------------
        Case "attack_move"
            ; Hold right mouse for camera
            MouseDown("right")
            Sleep(50)
            MouseUp("right")

        ; ----------------------------------------------------
        ; FORMATION MOVEMENT
        ; (Python sends absolute target positions)
        ; ----------------------------------------------------
        Case "formation_move"
            MouseMove($obj.x, $obj.y, 0)
            MouseClick("right")

        ; ----------------------------------------------------
        ; CAMERA TRACKING (yaw/pitch)
        ; ----------------------------------------------------
        Case "camera_delta"
            DllCall("user32.dll", "none", "mouse_event", _
                "dword", 0x0001, _
                "dword", $obj.dx, _
                "dword", $obj.dy, _
                "dword", 0, _
                "ptr", 0)

        ; ----------------------------------------------------
        ; UNKNOWN COMMAND
        ; ----------------------------------------------------
        Case Else
            ConsoleWrite("Unknown command: " & $cmd & @CRLF)

    EndSwitch

    Return True
EndFunc
