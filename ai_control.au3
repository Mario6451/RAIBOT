; ai_control.au3 — upgraded but 100% compatible with original

#include <File.au3>

Global $g_cmdFile   = "botcmd.txt"
Global $g_readyFile = "bot_ready.txt"
Global $g_stateFile = "botstate.txt"

; Fake state (AutoIt cannot read Roblox memory)
Global $g_x = 0
Global $g_y = 0
Global $g_angle = 0

; ---------------------------------------------------------
; SIGNAL READY
; ---------------------------------------------------------
FileDelete($g_readyFile)
FileWrite($g_readyFile, "ready")

; ---------------------------------------------------------
; WRITE STATE TO PYTHON
; ---------------------------------------------------------
Func _WriteState()
    Local $s = "x=" & $g_x & ";y=" & $g_y & ";angle=" & $g_angle
    FileDelete($g_stateFile)
    FileWrite($g_stateFile, $s)
EndFunc

; ---------------------------------------------------------
; APPLY COMMAND
; ---------------------------------------------------------
Func _ApplyCommand($cmd, $args)
    Switch $cmd

        ; ---------------- CAMERA KEYS (original 2016 binds) ----------------
        Case "cam_left"
            Send(",")

        Case "cam_right"
            Send(".")

        Case "cam_up"
            Send("{PGUP}")

        Case "cam_down"
            Send("{PGDN}")

        Case "cam_zoom_in"
            Send("i")

        Case "cam_zoom_out"
            Send("o")

        Case "cam_reset"
            Send("r")

        ; ---------------- MOUSE LOOK (raw delta) ----------------
        Case "mouse_delta"
            Local $dx = _Json_GetInt($args, "dx")
            Local $dy = _Json_GetInt($args, "dy")
            _Mouse_MoveRelative($dx, $dy)

        ; ---------------- RIGHT CLICK HOLD ----------------
        Case "right_down"
            DllCall("user32.dll", "none", "mouse_event", "dword", 0x0008, "dword", 0, "dword", 0, "dword", 0, "ptr", 0)

        Case "right_up"
            DllCall("user32.dll", "none", "mouse_event", "dword", 0x0010, "dword", 0, "dword", 0, "dword", 0, "ptr", 0)

    EndSwitch
EndFunc

; ---------------------------------------------------------
; MAIN LOOP
; ---------------------------------------------------------
While 1

    ; Read command file
    If FileExists($g_cmdFile) Then
        Local $json = FileRead($g_cmdFile)
        FileDelete($g_cmdFile)

        Local $cmd  = _Json_GetCmd($json)
        Local $args = _Json_GetArgs($json)

        _ApplyCommand($cmd, $args)
    EndIf

    ; Update fake angle (placeholder)
    $g_angle += 1
    If $g_angle > 360 Then $g_angle = 0

    _WriteState()

    Sleep(10)
WEnd


; ---------------------------------------------------------
; HELPERS
; ---------------------------------------------------------
Func _Mouse_MoveRelative($dx, $dy)
    DllCall("user32.dll", "none", "mouse_event", _
        "dword", 0x0001, _
        "dword", $dx, _
        "dword", $dy, _
        "dword", 0, _
        "ptr", 0)
EndFunc

Func _Json_GetCmd($json)
    Local $p = StringInStr($json, '"cmd"')
    If $p = 0 Then Return ""
    Local $q = StringInStr($json, '"', 0, 3, $p)
    Local $r = StringInStr($json, '"', 0, 4, $p)
    Return StringMid($json, $q + 1, $r - $q - 1)
EndFunc

Func _Json_GetArgs($json)
    Return $json
EndFunc

Func _Json_GetInt($json, $key)
    Local $p = StringInStr($json, '"' & $key & '"')
    If $p = 0 Then Return 0
    Local $colon = StringInStr($json, ":", 0, 1, $p)
    Local $comma = StringInStr($json, ",", 0, 1, $colon)
    If $comma = 0 Then $comma = StringInStr($json, "}", 0, 1, $colon)
    Local $val = StringStripWS(StringMid($json, $colon + 1, $comma - $colon - 1), 3)
    Return Int($val)
EndFunc
